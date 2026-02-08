Technical assessment write-up

I approached the technical assessment step by step, following the instructions in the email and INSTRUCTIONS.MD, which were straightforward.
For Part 1, I first wrote a small Python script to match timestamps between the datasets. I then went to the website and downloaded the data using their API code, selecting the required 6-hour intervals. Although I already had timestamp-matching logic which I wrote to decide which part of the ERA5 data to download, I realized it wasn’t best practice to rely on a separate script for this. Since the logic was simple and directly tied to the comparison itself, I moved it into the weather comparison file to keep the code more self-contained and easier to maintain.
I used AI as a helper for writing parts of the calculations and plotting code, while checking the logic and outputs myself.
For Part 2, I had already worked on a similar project during my internship at Almosafer and had prior experience with the Vercel AI SDK. I reviewed the documentation to refresh my memory and looked at older code that I wrote where I had used the Brave Search API as a tool. With that context, I was able to quickly implement the required parameters and debug the solution using documentation, prior knowledge, and some AI assistance.
spawnSync was new to me, so I spent time learning how it worked. I realized it was like concepts I had already seen in my systems programming course, particularly around child processes, which made it easier to understand.
At the end, I tested the tools using the provided questions and got good results. While reviewing everything, I noticed that error handling could be improved, so I added more checks, including in Part 1.



