Updating collection pages workflow ==================================

Overall workflow ----------------

1. Get latest code in `jessie` branch
    - Checkout branch `master`.
    - Pull `master`.
    - Checkout branch `jessie`.
    - Merge `master` into `jessie`.

2. Make changes to `include_file` for collection.

3. Test changes to collection page.

4. Commit changes.

5. Push changes.

6. Create pull request.

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

6.
