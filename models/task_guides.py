"""Editable learning content for the habitat's sample crew assignments."""

TASK_GUIDES = {
    "cognitive-test": {
        "goal": "Complete Alex's assigned psychomotor vigilance test (PVT) and record the reported reaction time.",
        "equipment": "The assigned PVT application or device and a quiet workspace.",
        "steps": (
            ("Prepare your workspace", "Sit comfortably at a quiet workstation in the living and working quarters. Use the same device and input method used for your previous tests."),
            ("Check the assigned protocol", "Confirm your name, the test date and trial number. Read the application's instructions and complete its practice block if provided."),
            ("Complete the test", "Respond to each stimulus as instructed by the application. Finish the full assigned session without pausing or switching to other tasks."),
            ("Record the reported result", "Record the application's median reaction time in milliseconds, with the test date and trial number. Note interruptions or device problems instead of treating an interrupted test as a routine result."),
            ("Review and complete", "Review the result with the assigned reviewer. On Alex's health page, Log a test includes Psychomotor vigilance · reaction time; its demonstration form does not modify the dataset. Mark this task complete after the test and review."),
        ),
    },
    "vo2max-test": {
        "goal": "Complete Milou's assigned aerobic fitness assessment and record the result for review.",
        "equipment": "Mission-approved exercise equipment, monitoring equipment and the assigned test protocol.",
        "steps": (
            ("Confirm the test method", "Check the assessment assigned by the mission medical officer. A supervised oxygen-consumption test and a wearable VO₂ max estimate are different methods; record which one you use."),
            ("Prepare with the test operator", "For a supervised test, let the trained operator set up the exercise equipment, breathing mask and monitoring sensors. Follow the assigned preparation instructions."),
            ("Follow the approved assessment", "Follow the operator's workload and recovery instructions. Do not turn a routine wearable estimate into an unsupervised maximal-effort test."),
            ("Record the result", "Record the reported VO₂ value in mL/kg/min, the observation date, test number and method. Keep a device estimate labelled as an estimate."),
            ("Review and complete", "Review the result with the assigned reviewer. Milou's health page includes a VO₂ max estimate option in Log a test; that form is a demonstration and does not change the dataset. Mark this assignment complete after the assessment and review."),
        ),
        "source": ("American Thoracic Society: cardiopulmonary exercise testing", "https://site.thoracic.org/advocacy-patients/patient-resources/cardiopulmonary-exercise-testing-cpet"),
    },
    "sleep-check": {
        "goal": "Review your overnight measurements and prepare a useful sleep report.",
        "equipment": "Your overnight wearable record and mission sleep log.",
        "steps": (
            ("Check the observation window", "Open your crew health page. Confirm the record belongs to you and covers the overnight sleep period you want to review."),
            ("Check the recording quality", "Look for missing readings, sensor removal or interruptions. Mark these as gaps rather than treating them as a change in health."),
            ("Review the overnight pattern", "Compare overnight heart rate, HRV and sleep score with your own recent records. Note changes for review; a dashboard score alone does not establish a diagnosis."),
            ("Add your sleep experience", "In your mission sleep log, note bedtime, wake time, awakenings, how rested you feel, and disturbances such as noise or schedule changes."),
            ("Prepare your handover", "Share unexpected patterns or ongoing sleep concerns with the mission medical officer. Include the observation date, recording gaps and your notes before marking this task complete."),
        ),
    },
    "medical-check": {
        "goal": "Collect a clear blood-pressure record for the mission medical officer.",
        "equipment": "Mission-approved upper-arm blood-pressure monitor, correctly sized cuff and health log.",
        "steps": (
            ("Prepare for measurement", "Follow the device instructions and mission procedure. Avoid exercise, smoking and caffeine for 30 minutes beforehand, and empty your bladder."),
            ("Rest and position yourself", "Sit quietly for at least five minutes, with your back supported and feet flat. Support your arm so the cuff is at heart level. Do not talk during measurement."),
            ("Fit the cuff", "Place the correctly sized cuff on bare skin, following the monitor's placement instructions. Do not measure over clothing."),
            ("Take two readings", "Start the monitor and stay still. Record systolic pressure, diastolic pressure and the time. Wait one minute, then take and record a second reading."),
            ("Record and hand over", "Save both readings in the mission health log with any device errors or symptoms. Follow the mission medical officer's instructions for interpretation and follow-up; do not change medication based on this guide."),
        ),
        "source": ("American Heart Association: measuring blood pressure", "https://www.heart.org/en/health-topics/high-blood-pressure/understanding-blood-pressure-readings/monitoring-your-blood-pressure-at-home"),
    },
    "exercise-check": {
        "goal": "Document how you recovered after your scheduled exercise session.",
        "equipment": "Your assigned exercise plan, wearable record and mission exercise log.",
        "steps": (
            ("Finish with the assigned cool-down", "Follow the cool-down in your approved exercise plan. General guidance recommends gradually reducing intensity over five to ten minutes instead of stopping vigorous activity abruptly."),
            ("Check the wearable record", "Confirm your sensor recorded the correct workout and recovery period. Note missing samples or poor contact before interpreting the graph."),
            ("Review recovery", "Open your crew health page and inspect the post-workout heart-rate trend. Compare with your own similar sessions, noting the workout intensity and measurement times rather than applying a universal recovery target."),
            ("Log how the session felt", "Record the activity, duration, perceived effort and any discomfort in the mission exercise log. Report concerning symptoms to the mission medical officer and follow the mission response procedure."),
            ("Complete the handover", "Share the recovery record and any concerns with the assigned reviewer. Mark the task complete once the review has been carried out."),
        ),
        "source": ("American Heart Association: warm up and cool down", "https://www.heart.org/en/healthy-living/exercise-and-physical-activity/fitness-basics/warm-up-cool-down"),
    },
}
