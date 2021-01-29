# Smart Love Note 
This was an anniversary project for my wonderful girlfriend. Using a raspberry pi zero and a 2.9 inch e-paper display, the device output a message from the stored message file to the display. Updating multiple times a day with the ability to override the scheduled love note display. The stored text file can be added to or overridden with a unique message for a set time period that does not get saved to the love note file.

![heart shape with electronic hardware](https://github.com/LazerGerraldo/E-Paper-Love-Note/blob/master/miscMedia/Early%20Example.jpg)

## Table of Contents
- [Code Overview](#Code-Overview)
    - [Display Interface](#Display-Interface)
    - [Email](#Email)
- [Hardware](#E-Paper-Display)
    - [Pi Setup](#Pi-Setup)
    - [E-Paper Display](#E-Paper-Display)
    - [Case](#Case)

## Code

## Display Interface
Interfacing with the display was a difficult part of coding for me, and out of my comfort zone for the most part. I had a lot of help from a software engineering roommate and the manufacture website for the model of e-Paper display I had, the [2.9inch e-Paper Module B](https://www.waveshare.com/wiki/2.9inch_e-Paper_Module_(B)). Using the given example code for the display, I had a solid foundation for starting my love note output. Rather than creating something from scratch, I widdled down the parts of the example code that worked for me.

## Email   
I started learning about how to pull emails from the Gmail client.
Using an article by [Humberto Rochas,](https://humberto.io/blog/sending-and-receiving-emails-with-python/) on sending and receiving emails with python gave me a great start for getting emails from gmail to python. 

In order to get past Googles security I had to grant less secure app access. To do that I navigated to 
````Google Account Settings > Security > Less Secure App Access ```` at the bottom of the page, set that to __on__. This got me past the ````[AUTHENTICATIONFAILED] Invalid credentials (Failure)```` error that Rochas example was giving me. 

As for using the IMAP python function I found [this article](https://github.com/ikvk/imap_tools) very helpful with IMAP formatting. From there I was able to find a way to pull emails filtered by my personal email.

I ended up using two imap.search functions that worked for me. The first was helpful for reading emails specifically from my personal email to the project email, the second focused on the emails from me as well as making sure they were unread. Once read by the search function the email would be marked as read which is very helpful for the final product but not helpful for the testing phases of the code. 

````
status, data = mail.search(None, 'FROM My-Personal-Email') #use for testing
status, data = mail.search(None, 'FROM My-Personal-Email UNSEEN') #use for final version that will uncheck email
````
This code needs the file EmailLogin.txt that should be saved in /home/pi/ directory with three lines including an email, that emails password, and a personal email that the mail search will identify target messages by. There is an example file in the GitHub directory.

## Hardware

I used a raspberry pi zero and purchased an AIO kit from CanaKit. The package comes with an power cord and a formatted SD card with NOOBS OS to save some time. 

## Pi Setup
Following the [SSH guide from  the raspberry pi website](https://www.raspberrypi.org/documentation/remote-access/ssh/passwordless.md) I was able to get a SSH key from the Pi to associate with github in order to clone and push changes if needed. The following commands were used to copy the pi SSH key and add it to my account on github. The SSH repository link is found under the code tab on the main project github page.
````
cd .ssh
cat id_rsa.pub
````

After adding the API key to my github account page I cloned the repository on the pi with the following commands.

````
sudo apt-get install git
git clone git@github.com:LazerGerraldo/E-Paper-Love-Note.git
git checkout -f HEAD
````
Additionally the installation library for the e-Paper display is required found on the [Waveshare github page.](https://github.com/waveshare/e-Paper) I will include the required commands below.

````
sudo apt-get update
sudo apt-get install python3-pip
sudo apt-get install python3-pil
sudo apt-get install python3-numpy
sudo pip install RPi.GPIO
````
````
sudo vim /etc/rc.local
added line in rc.local
````
In order for the pi to start the program on boot the command `python3 /home/pi/E-Paper-Love-Note/main.py` was added to the file `rc.local` as shown in the tab below.

<details>
  <summary>rc.local file changes</summary>
    
    #!/bin/sh -e
    #
    # rc.local
    #
    # This script is executed at the end of each multiuser runlevel.
    # Make sure that the script will "exit 0" on success or any other
    # value on error.
    #
    # In order to enable or disable this script just change the execution
    # bits.
    #
    # By default this script does nothing.
    # Print the IP address
    _IP=$(hostname -I) || true
    if [ "$_IP" ]; then
      printf "My IP address is %s\n" "$_IP"
    fi
    python3 /home/pi/E-Paper-Love-Note/main.py
    exit 0
</details>

The pi did not realize what the correct time zone was. After changing the time zone with `sudo raspi-config` the program worked.

## E-Paper Display 
The display hooked right up to the pi. There was not a lot of documentation as to what pins on the display connected to the pi. I found the [raspberry pi GPIO pin-out](miscMedia/gpio.png), and followed the manufacture website as well as the table below.


| Function   | Wire Color | Pi Pin Number |
|------------|--------------------|---------------|
| VCC(3.3 V) |  Grey              |       01      |
| GND        |  Brown             |       06      |
| DIN        |  Blue              |       19      |
| CLK        |  Yellow            |       23      |
| CS         |  Orange            |       24      |
| DC         |  Green             |       22      |
| RST        |  White             |       11      |
| BUSY       |  Purple            |       18      |


*I actually had the ground wire connected to pin 03 GPIO02 rather than the ground during the whole testing process.

## Case

This was one of the areas that I was more comfortable in at the beginning of this project. I used OnShape a free CAD software with tons of video tutorials online. You can see the project [case design files here](https://cad.onshape.com/documents/de2a48e93b168b76a3072b45/w/6d8c1324762ceb9f50b6db77/e/b73ae14c0cc5d6f088d5bd19).

Most of the design process involved measurements. Most of my time was spent using calipers and measuring things multiple times, however these schematics for the [raspberry pi zero](https://i.stack.imgur.com/LHeqV.png), and the [e-Paper display](https://www.waveshare.com/img/devkit/LCD/2.9inch-e-Paper-Module/2.9inch-e-Paper-Module-size.jpg) from the manufacture website were very helpful. The display was on a PCB with standoffs making the height measurements a bit difficult.

Looking at using 3x "hex socket head countersunk screw m3 x 8mm" to attach the two parts of the case together two in each corner and one at the base of the heart. And threaded inserts.
