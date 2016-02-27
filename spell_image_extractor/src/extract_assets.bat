@echo off
java -jar ../disunity/disunity.jar -f texture2d bundle-extract data/*.unity3d

java -jar ../disunity/disunity.jar -f texture2d extract data/*.unity3d

java -jar ../disunity/disunity.jar -f texture2d bundle-extract data/*.assets

java -jar ../disunity/disunity.jar -f texture2d extract data/*.assets
