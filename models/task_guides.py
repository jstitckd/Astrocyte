"""Editable learning content for the habitat's sample crew assignments."""

TASK_GUIDES = {
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
