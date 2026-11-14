"""Optional browser QA. Requires playwright; not part of unittest discovery.

Start Streamlit first, then:
  python tests/browser_smoke.py --url http://127.0.0.1:8501
Pass --browser /path/to/chrome to use an existing Chrome installation.
"""
import argparse
from pathlib import Path

from playwright.sync_api import expect, sync_playwright


def run(url, browser_path, screenshots):
    # Standalone script: the application itself does not require Playwright.
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, **({"executable_path": browser_path} if browser_path else {}))
        desktop = browser.new_context(viewport={"width": 1512, "height": 1100}, device_scale_factor=1)
        page = desktop.new_page()
        failures = []
        page.on("pageerror", lambda exc: failures.append(str(exc)))
        response = page.goto(url)
        assert response.status == 200
        expect(page.get_by_role("heading", name="A little closer to home.")).to_be_visible()
        frame = page.frame_locator('iframe[title="components.base_map.astrocyte_base_map"]')
        expect(frame.locator('[data-area="sleep"]')).to_be_visible()
        frame.locator('[data-area="sleep"]').hover()
        expect(frame.locator("#preview-name")).to_have_text("Sleeping quarters")
        expect(frame.locator("#preview-tasks")).to_contain_text("overnight heart rate, HRV and sleep duration")
        expect(page.get_by_text("0 of 15 tasks completed", exact=True)).to_be_attached()
        if screenshots:
            screenshots.mkdir(parents=True, exist_ok=True)
            page.screenshot(path=str(screenshots / "desktop.png"), full_page=True)
        titles = {
            "sleep": "Make room for recovery.", "exercise": "Keep moving, one sol at a time.",
            "medical": "A clearer picture of how you feel.", "nutrition": "Fuel for the journey ahead.",
            "wellbeing": "A little space to check in.", "eva": "Prepare for the world outside.",
        }
        for area, title in titles.items():
            print("Checking map route:", area, flush=True)
            frame.locator(f'[data-area="{area}"]').click()
            expect(page.get_by_role("heading", name=title)).to_be_visible()
            assert page.get_by_test_id("stException").count() == 0
            page.get_by_role("button", name="⌂ Base overview").click()
            expect(page.get_by_role("heading", name="A little closer to home.")).to_be_visible()
        frame.locator('[data-area="exercise"]').focus()
        page.keyboard.press("Tab")
        expect(frame.locator('[data-area="sleep"]')).to_be_focused()
        expect(frame.locator("#preview-name")).to_have_text("Sleeping quarters")
        frame.locator('[data-area="sleep"]').press("Space")
        expect(page.get_by_role("heading", name=titles["sleep"])).to_be_visible()
        page.get_by_role("button", name="⌂ Base overview").click()
        region = frame.locator('[data-area="medical"]')
        region.focus()
        expect(frame.locator("#preview-name")).to_have_text("Medical bay")
        region.press("Enter")
        expect(page.get_by_role("heading", name=titles["medical"])).to_be_visible()
        expect(page.locator(".js-plotly-plot").first).to_be_visible()
        if screenshots:
            page.screenshot(path=str(screenshots / "dashboard.png"), full_page=True)
        page.get_by_label("Notes", exact=True).fill("Browser-verified symptom observation")
        page.get_by_role("button", name="Save check-in", exact=True).click()
        expect(page.get_by_text("Check-in saved for this session.", exact=False)).to_be_visible()
        page.get_by_test_id("stCheckbox").filter(has_text="Review available vital signs").locator("label").click()
        expect(page.get_by_label("Review available vital signs", exact=True)).to_be_checked()
        page.get_by_role("button", name="⌂ Base overview").click()
        expect(page.get_by_text("1 of 15 tasks completed", exact=True)).to_be_visible()
        page.get_by_role("button", name="↧ Data & exports").click()
        with page.expect_download() as download:
            page.get_by_role("button", name="↓ Export session check-ins & tasks (JSON)").click()
        assert download.value.suggested_filename == "astrocyte_session.json"
        # Real upload path, including the on_change validator and atomic error handling.
        page.get_by_role("combobox", name="Data source", exact=True).click()
        page.get_by_role("option", name="Imported CSV", exact=True).click()
        page.locator('input[type="file"]').set_input_files(str(Path(__file__).resolve().parents[1] / "data" / "sample_readings.csv"))
        expect(page.get_by_text("IMPORTED SNAPSHOT", exact=False)).to_be_visible()
        page.locator('input[type="file"]').set_input_files({"name": "invalid.csv", "mimeType": "text/csv", "buffer": b"wrong,headers\n1,2"})
        expect(page.get_by_text("Your previous import is still loaded.", exact=False)).to_be_visible()
        assert page.get_by_test_id("stException").count() == 0
        assert not failures, failures

        mobile = browser.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True, device_scale_factor=1)
        phone = mobile.new_page()
        phone.goto(url)
        expect(phone.get_by_role("heading", name="A little closer to home.")).to_be_visible()
        # Streamlit may initially open the sidebar; collapse it for the map.
        collapse = phone.get_by_test_id("stSidebarCollapseButton").get_by_role("button")
        if collapse.is_visible():
            collapse.click()
        phone_frame = phone.frame_locator('iframe[title="components.base_map.astrocyte_base_map"]')
        phone_frame.locator('[data-area="wellbeing"]').tap()
        expect(phone_frame.locator("#preview-name")).to_have_text("Greenhouse / common room")
        expect(phone_frame.locator("#mobile-areas button")).to_have_count(6)
        phone_frame.get_by_role("button", name="05 Greenhouse / common room", exact=True).tap()
        # Wait for the component's asynchronous height message before capturing it.
        expect(phone_frame.locator("#open-dashboard")).to_be_visible()
        if screenshots:
            phone.screenshot(path=str(screenshots / "mobile.png"), full_page=True)
        phone_frame.locator("#open-dashboard").tap()
        expect(phone.get_by_role("heading", name=titles["wellbeing"])).to_be_visible()
        assert phone.get_by_test_id("stException").count() == 0
        browser.close()
        print("PASS: six map routes, hover, keyboard Tab/Enter/Space, rendered Plotly chart, saved form, task progress, JSON download, CSV upload/rejection and mobile tap navigation")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://127.0.0.1:8501")
    parser.add_argument("--browser")
    parser.add_argument("--screenshots", type=Path)
    args = parser.parse_args()
    run(args.url, args.browser, args.screenshots)
