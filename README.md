# AmazonScraperApp

<br />

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

This project was a beginner/intermediate project that I took on personally to learn about web scraping and a bit about JavaScript. I figured one of the best ways would be scraping a website that I often visit - Amazon.com. I found many blockers that such as User-Agents, but ultimately the application functioned properly as expected.

The web application takes two inputs:
* Your budget you have to spend
* List of URLs of Amazon products you wish to purchase

Of course, some products are more diffficult to parse so at the moment only 'In stock' prodcucts can be scraped and only ones bought in US Dollars. After crawling and getting the necessary information the web app will output the results of the products you can purchase and how much you are left with. An extra feature that I will looking to add is setting a reminder (given certain settings) to notify someone when a low price is found.

Obviously, the extra feature would not be bombarding someone with hundreds of emails, but instead will run temporarily at a set interval. In addition, the person can extract the information to a seperate CSV file.

A list of commonly used resources that I find helpful are listed in the acknowledgements.

### Built With

This section should list any major frameworks that you built your project using. Leave any add-ons/plugins for the acknowledgements section. Here are a few examples.
* [Bootstrap](https://getbootstrap.com)
* [JavaScript](https://www.javascript.com)
* [Python](https://www.python.org)



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* pip/pip3
  ```sh
  pip install -r requirements.txt
  ```

<!-- USAGE EXAMPLES -->
## Usage

1. Run flask
   ```sh
   flask run
   ```

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.


<!-- CONTACT -->
## Contact

Your Name - [@your_twitter](https://twitter.com/your_username) - email@example.com

Project Link: [https://github.com/your_username/repo_name](https://github.com/your_username/repo_name)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
* [GitHub Emoji Cheat Sheet](https://www.webpagefx.com/tools/emoji-cheat-sheet)
* [Img Shields](https://shields.io)
* [Choose an Open Source License](https://choosealicense.com)
* [GitHub Pages](https://pages.github.com)
* [Font Awesome](https://fontawesome.com)





<!-- MARKDOWN LINKS & IMAGES -->
[product-screenshot]: App.png
