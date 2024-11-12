# SIGMusic DAW Project

## Project Description
The project is a digital audio workstation (DAW) that allows users to create and edit music. Users should be able to load, save, and edit audio files, as well as create their own audio files using the software. The software should also have the ability to apply filters to audio files, such as lowpass and highpass filters.

## Setup
To streamline dependency installation, it's recommended to set up a virtual environment.

1. **Create a Virtual Environment**:
    - Python3:
        ```bash
        python3 -m venv venv
        ```
    - Python2:
        ```bash
        python -m venv venv
        ```


2. **Activate the Virtual Environment**:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - MacOS/Linux:
     ```bash
     source venv/bin/activate
     ```

3. **Install Dependencies**:
   ```bash
   make install
   ```

## Development

1. **Branching and Pulling Latest Changes**:
   
   Create a new branch to work on:
     ```bash
     git checkout -b <firstname-lastname>
     git pull origin main
     ```

2. **Adding New Dependencies**:
   
   Ensure to update the requirements.txt file after adding new dependencies:
     ```bash
     make update
     ```

3. **Pushing Changes and Making Pull Requests**:
   
   After completing your work, push your branch to the repository and make a pull request to the main branch:
     ```bash
     git push origin <firstname-lastname>
     ```

4. **Starting Work**:
   
   Every time you start working, pull the latest changes and update dependencies:
     ```bash
     git pull origin main
     make update
     ```

## TODO 
### Frontend
- [ ] get some buttons, sinusoid rendering going

### Backend
- [ ] Generate and save sinusoid waves programmatically (high priority!!!).
- [ ] Implement sound import, export for **WAV**, MP3, AIFF formats.
- [ ] Custom filters + extensions!

### Other
- [ ] MIDI later... 
