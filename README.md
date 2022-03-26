[![tests](https://github.com/niklas-rittmann/StrangerDanger/actions/workflows/tests.yml/badge.svg)](https://github.com/niklas-rittmann/StrangerDanger/actions/workflows/tests.yml)

## :cop: StrangerDanger

## :mag: Summary
**StrangerDanger** is your private security system. Connect stranger danger to existing surveileince cameras to detect intruders in defined areas using machine learning.

## :construction: Roadmap

- [x] Create different fences (Circular, Rectangular and Pentagon)
- [x] Integrate the first image classifier
- [x] Create an Email constructor to send the prediction images to different receivers
- [x] Build a class the hold different fences, the email constructor and a classifier
- [x] Integrate a database to hold the fences, predictions, classifiers and email settings
- [x] Build the event based image detection
- [ ] Integrate an API that allows you to:
  - [x] Authentificate
  - [x] Specify fences
  - [ ] Select different image classifiers
  - [x] Start and Stop the detection service
  - [ ] Setup Email Settings (e. g. Receivers)
  - [ ] Get the last predictions sorted by time
- [ ] Build docker image to simplify use
- [ ] Build a web based user interface to serve the API
- [ ] Add different image streaming services
- [ ] Detect different entities like dogs as well
- [ ] Trigger event when Stranger is detected
