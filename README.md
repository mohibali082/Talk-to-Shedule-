# Talk-to-Shedule-
Talk to Shedule

Description

Talk to Shedule is a generative AI  project that allows users to provide a voice message, which is then processed to create a calendar. This makes scheduling tasks and managing events effortless and hands-free.
This project converts speech into a scheduled day-to-day calendar, making planning effortless and hands-free.

Features

Converts speech to text.

Extracts dates and times from speech input.

Automatically schedules events in a calendar format.

Runs in Google Colab, requiring no local setup.

How to Run

Open the notebook in Google Colab.

Run the cells in sequence.

Upload a voice file 

View the generated calendar output.

Dependencies

To ensure smooth execution, install the required dependencies:

!pip install openai-whisper
!sudo apt update && sudo apt install ffmpeg
pip install googletrans==4.0.0-rc1
pip install langdetect
!pip install httpcore==0.15.0
pip install googletrans==4.0.0-rc1 httpx==0.13.3
pip install dateparser


Example Usage

Provide a voice message like: "Meeting on Monday at 3 PM with John".

The system processes the input and creates an event in the calendar.

Output format:

| Date       | Time  | Event        |
|------------|-------|-------------|
| 2025-02-19 | 15:00 | Meeting with John |

Contributing

If you'd like to improve this project, feel free to fork the repository and submit a pull request.

License

This project is open-source under the MIT License.

