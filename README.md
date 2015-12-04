#workingfrom Slack command

**We all know the feeling.**

You have a doctor's appointment for that thing on your neck (ew). You tell people in a Slack channel you're working from home, but the message is quickly lost in the hustle and bustle of cat gifs and food announcements. What to do?

You're trying to find Walter, but you don't even know if he's in the office. Where is Walter???

You get dozens of emails about people being out of office or working from home, and you think "Who are these people? Why are they telling me this? How did I get here?"

This Slack command solves all of your problems, except for most of them and also that thing on your neck.

To let people know you're at home in your PJs, simply type in any Slack channel 

    /workingfrom home
    
If you're in the San Francisco office, 

	/workingfrom SF
	
On vacation? 

	/workingfrom Out of office until December 10th.

Where is Walter?? You can find out! Just enter Walter's username:

	/workingfrom @walter

You can also indicate where you're typically working from with the `--default` option:

	/workingfrom SF --default
	
This way, people can tell where you're likely to be, even if you haven't used /workingfrom recently.

###Using with Slack
The easiest way to deploy this code is to run it as a [Heroku app](https://devcenter.heroku.com/articles/getting-started-with-python-o). Then, create a Slack command for your team and hook it up.

###License
The MIT License (MIT)

Copyright (c) 2015 Mat Leonard

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
