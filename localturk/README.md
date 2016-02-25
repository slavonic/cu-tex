# localturk

Config files and data files for localturk - a utility to help review large datsets.

# Introduction
Please, read localturk README: https://github.com/mkroutikov/localturk

# Use for hyphenation patterns review

## Installation

1. install `node.js`, see https://nodejs.org/en/ or use your favorite package manager.

2. clone repository
   ```bash
   cd ~/git
   git clone https://github.com/mkroutikov/localturk.git
   ```
3. install dependencies (utility `npm` should be installed as part of `node` installation. Some Linux
   distributins though use a separate package for it. If so - install `nmp` first!
   ```
   cd localturk
   npm install
   ```
   
4. copy `PonomarUnicode.woff` to the current directory (or use `-s` switch to specify directory)

## Running it

1. cd back to this directory and start localturk
    ```bash
    cd ~/git/cu-tex/localturk
    node ~/git/localturk/localturk.js template.html words.csv reviewed.csv -s. --batch_size 15
    ```

4. it should automatically open a browser window. If not, direct your browser to http://localhost:4321

5. start reviewing. Click "Submit" when you are satisfied with the current values.

6. at any moment you can `Ctrl+C` to stop server. Your work will **not** be lost! Next time you start
   localturk it will continue from the point where you left.

7. Do not forget to commit `reviewed.txt`

 ## Explanation
 localturk reads `words.csv` and writes result to `reviewed.csv`. It "remembers" where you left off by looking
 at the number of rows in the `reviewed.csv`. Never update `words.csv`! Only safe operation is appending more data to it.
 Html template is used to present the data and style the UI.
 
 Command-line switch `-s` provides "static" directory for the localturk - this is for serving static files to the client
 (depending on template you may need this). In our case we need this because style refers to webfont - need to point
 to the directory where webfont resides. Use `-s .` if you copied webfont file to current directory. Or provide the
 external directory where font file can be found.
 
 Command-line switch `--batch_size` defines how many entries per page are displayed.