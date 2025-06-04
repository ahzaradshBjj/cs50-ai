import os
import random
import re
import sys
import pandas as pd

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    probs = {}

    # if corpus[page]:
    #     # get all the values(links)
    #     values =  set()
    #     for value in corpus.values():
    #         values.update(value)

    #     # prob of choosing one of the values(links)
    #     prob_links = damping_factor / len(values)
    #     # prob of choosing one of all pages
    #     prob_pages = (1 - damping_factor) / (len(corpus))

    #     # get all the pages
    #     keys_set = set()
    #     for key in corpus:
    #         keys_set.update([key])

    #     # if there are more pages than links(no link to at least one page)
    #     if len(values) < len(corpus):
    #         difference = keys_set.difference(values)

    #         for page_nolink in difference:
    #             probs[page_nolink] = prob_pages

    #     for link in values:
    #         # if link not in difference:
    #         probs[link] = prob_links + prob_pages

    #     # Ensure that the sum of proves is 1
    #     # probs = list(probs.values())
    #     # if (sum(probs) == 1):
    #     #     print("it is okay")
    # # if not outgoing links
    # else:
    #     prob_pages = 1 / len(corpus)
    #     for k in corpus:
    #         probs[k] = prob_pages

    # # add all pages of corpus
    # for key in corpus:
    #     probs[key] = 0

    # # get number of pages
    # n_pages = len(corpus)

    # # if page has links
    # if corpus[page]:
    #     links = corpus[page]
    # # "links" are going to be all the pages
    # else:
    #     links = corpus.keys()

    # # loop through each page
    # for page in probs:
    #     # prob of choosing one of all pages
    #     probs[page] = (1 - damping_factor) / n_pages
    #     # if the page is in links
    #     if page in links:
    #         probs[page] += damping_factor / len(links)

    # if page has links, use them, otherwise assign all keys
    links = corpus[page] if corpus[page] else corpus.keys()

    # Number of pages in corpus
    n_pages = len(corpus)

    # Prob of choosing any page at random
    random_prob = (1 - damping_factor) / n_pages

    # Prob of choosing a linked page
    link_prob = damping_factor / len(links)

    # Assign probs
    for p in corpus:
        # Base random probability for all pages
        probs[p] = random_prob
        # If the page is in the links, add link probability
        if p in links:
            probs[p] += link_prob

    return probs
    # raise NotImplementedE/7rror


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    pagerank = {}

    # Get all pages of corpus
    for page in corpus:
        pagerank[page] = 0

    # Choose a page at random
    page = random.choice(list(corpus.keys()))

    # Loop through all samples
    for _ in range(n):
        # Keep count of visiting that page
        pagerank[page] += 1

        # Get the model
        model = transition_model(corpus, page, damping_factor)

        # Get the pages and probs out of the model
        pages = list(model.keys())
        probs = list(model.values())
        # Choose the pagg randomly but given the probs of each page
        page = random.choices(pages, probs)[0]

    # Normalize Pagerank
    normalized_pagerank = {}
    for page in pagerank:
        normalized_pagerank[page] = pagerank[page] / n
    # for sample in range(n):
    #     # first page will be at random
    #     if sample == 0:
    #         # get all the values(links)
    #         values =  set()
    #         for value in corpus.values():
    #             values.update(value)

    #         # Choose link at random
    #         random_link = random.choice(list(values))
    #         result = transition_model(corpus, random_link, damping_factor)
    #     else:
    #         for link in values:
    #             if link != random_link:
    #                 result = transition_model(corpus, link, damping_factor)
    #         # print("ga")
    #         # result = transition_model(corpus,, damping_factor)
    return normalized_pagerank
    # raise NotImplementedError


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    pagerank = {}
    number_pages = len(corpus)

    # At the beginning
    for page in corpus:
        pagerank[page] = 1 / number_pages

    threshold = 0.001
    new_pagerank = pagerank.copy()

    while True:
        for p in corpus:
            # pagerank formula
            total = (1 - damping_factor) / number_pages
            # Loop again through all pages
            for i in corpus:
                # Prob of going from i to page (given that i am in page,
                # the prob of coming from i)
                if p in corpus[i]:
                    total += damping_factor * (pagerank[i] / len(corpus[i]))
                # if it does not have a link
                if not corpus[i]:
                    total += damping_factor * (pagerank[i] / number_pages)
            # Assign the new total
            new_pagerank[p] = total

        converged = True
        # Iterates through each page
        for page in pagerank:
            diff = abs(new_pagerank[page] - pagerank[page])
            if diff >= threshold:
                converged = False
                break

        if converged == True:
            break
        else:
            pagerank = new_pagerank.copy()

    return new_pagerank
    # raise NotImplementedError


if __name__ == "__main__":
    main()
