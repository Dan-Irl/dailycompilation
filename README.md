# Daily Compilation

## Introduction

Daily Compilation is a Python project aimed at automating the process of creating daily video compilations from Twitch clips. This project serves as a showcase of integrating multiple APIs and classes to create a fully functional system. The purpose behind this project is not only to educate myself in the intricacies of API integration and system design but also to provide a tangible project for my portfolio. The also helped me get introduced to the concpet of automatic generative content as this code could easily be run in a containerized environment such as docker to coninusly generate daily content.

The system operates by scraping daily clips from Twitch, collecting metadata through the Twitch API, and then downloading these clips. It utilizes the MoviePy library to edit these clips together, overlaying metadata such as the clip title and creator name, and finally renders the compilation video. The project also prepares all video information, including title and description, and uploads the video to YouTube using the Google YouTube API V3 and OAuth2 for authentication.

## Features

- **Clip Collection**: Uses the Twitch API to scrape daily clips and collect metadata.
- **Video Editing**: Combines clips into a compilation with metadata overlays using MoviePy.
- **YouTube Upload**: Prepares video information and uploads the compilation to YouTube with the appropriate metadata.

## **Project Structure**
- **Clip.py**: A data class containing all the features of a clip object.
- **twitch_api.py**: Handles authentication and connection to the Twitch API.
- **twitchclip.py**: Prepares clip data using Selenium for web scraping and downloads clips.
- **editor.py**: Combines clips into a compilation and adds metadata overlays; prepares compilation metadata.
- **youtube.py**: Manages authentication to YouTube API using OAuth2 and uploads the video with metadata.
- **main.py** - Main runtime for application

## **Outcomes**

This project had the following learning outcomes:

- Gaining a deeper understanding of object-oriented programming and the seamless interaction between classes.
- The construction of API requests, including both POST and GET methods.
- Enhancing my knowledge of authentication mechanisms, such as API keys and OAuth protocols.

A resulting demo video can be seen here: [youtube](https://www.youtube.com/watch?v=SV0aSnYj29Y) 

