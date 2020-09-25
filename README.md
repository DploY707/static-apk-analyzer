This Project is for APK Analysis

# How to install this project
1. $ cd [root directory of this project]
2. $ docker build -t android-analyzer ./

# How to Use it
1. Move your APK that want you to analyze to [./data] directory
   (in this case, your APK name should not have whitespace (' ') !!)
2. $ docker run -it --rm -v [host APK directory path]:/root/workDir/data android-analyzer
