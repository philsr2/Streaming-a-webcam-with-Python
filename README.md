# Streaming-a-webcam-with-Python
This started out as a really horrible webcam streamer sending a frame at a time with SCP.  Now, with a few AI suggested improvements it can hold fairly steady sending back to 3 end users (browsers)

While I was using SCP to send each frame, it would take 1.7 seconds each, definitely not acceptable.
I got an AI (I've only ever used the various freely available ones IE: the land of lobotomized children-AI, so with a sub and tokens ymmv) to setup a small flask server which would accept a JSON encoded image and save it to disk.  I was also saving each frame to disk before sending it on my client-origin side.  IE webcam->disk->JSON encode->send to server->disk.

Yesterday I asked Chatgpt how I could improve that, maybe by avoiding disk writes and using websockets (absolute newbie, this is my first websocket code) to get the frames to a browser page.

My server setup is fairly simple, a Fedora 43 server with python (my main website runs under Apache and modperl, i have https running solely under a Go server that keeps the certs up to day with autocert)

I keep this new websockets server in a narrow lane, only my home IP can send to it.  Separate FW zones using Firewall-cmd makes it a dream to keep safe (ssh is limited to my FW's home zone too so my logs don't get clogged up with all the bot login attempts).

Now I have three pieces of this web streamer.  Sendit.py which takes frames from the webcam and sends them to Server.py which serves them to the webcam.html page on port 5000 (chosen arbitrarily, mainly because I had that open in my FW home zone for test servers)

Things still to do:
  1.  fix error handling, the server doesn't crash when i browser closes now, but still have unhandled errors.
  2.  multiple webcams, would make this useful as a multi-user video chat.
  3.  drop frames when it gets out of sync, needs to be closer to realtime.
  4.  look into different quality streams.  25% jpeg quality only uses about 2.5mpbs, while 90% uses more like 7.5mbps
  5.  needs compression or maybe ffmpeg to send the stream, probably an actual video format versus image by image
  6.  other things I haven't thought of yet (like TLS connections)  July16 Note: implementing SSL/TLS in my chat server was incredibly easy, add an import for ssl add two other lines to set the contect and change the serve line and print noting where it started.  Voila, security...
