Updating collection pages workflow ==================================

I. Overall workflow ----------------

1. Get latest code in `jessie` branch
    - Checkout branch `master`.
    - Pull `master`.
    - Checkout branch `jessie`.
    - Merge `master` into `jessie`.

2. Make changes to `include_file` for collection.

3. Test changes to collection page.

    1. open terminal
    2. run op-coll and validate and update if necessary
    3. run op-pages -i coll tag [--really-force]
    4. run open url

4. Commit changes.

5. Push changes.

6. Create pull request on Bit Bucket.

7. Notify Doug.

Refer to this tutorial on information about how to use [Markdown](https://daringfireball.net/projects/markdown/basics):

To create the html pages after editing the file in Markdown in TextWrangler, go to Terminal and type `op-pages -f -i [Coll. Tag]`
This should create the html page and give you a path to the new html page
Then type `open /path/`

Once things have been edited and are ready to go:

1.  commit changes in SourceTree
2.  push items to `jessie`

pull request

3.  go to bitbucket site in the OPenn directory
4.  hover over three dots, click create pull request

5.  pull master, merge master into jessie


II. Creating a new collection

Check op-coll on dev server

open up settings file

