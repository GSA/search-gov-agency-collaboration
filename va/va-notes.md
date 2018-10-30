# Notes on Indexing VA.gov
Questions and Answers, in both directions

## Prioritization

Q from Dawn to VA 10/29:
Thank you for showing which microsites are top 10, and I see also you made a 100 group and a 200 group. Are the sites currently without a priority somewhere in between 11 and 99, or are they low enough priority not to have a ranking at this time? Thanks.

A: 100 are more important than 200, but can go in any order, at any time.

Q: If there is no priority, are those lower than 200? or higher than 100?
  
A: If there is no priority assigned yet, it is _very likely_ that these are more important than 100-level. I am working on getting at least a rough order in for those.
  
## Technical  

Q: Are urls case sensitive?

A: No. They are transcribed as derived from internal documents, but no URL as far as I am aware is specifically case sensitive.

Q: Can you add a block at the **top** of www.va.gov/robots.txt, that would target our crawler at the specific allowed folders within that subdomain? e.g. 
```
User-agent: usasearch
Disallow: /
Allow: www.va.gov/health
Allow: www.va.gov/vaforms
Allow: www.va.gov/homeless
Allow: www.va.gov/about_va
etc.
```
* Note the request to put the block as the first directive in the robots.txt, for some reason our crawler will only check at the top, but we'd rather index your content than make the crawler more flexible at this point.

A: Shouldn't be a problem, I'll let you know when that's done.

* Follow up: Awesome - just to be clear we're asking for one Allow line per folder, this is 79 folders.

  * The task is in, will let you know when live. I just want to make sure that the `Disallow: /` directive won't intefere with indexing pages in `sitemap-dynamic` -- for example, preview.va.gov/health-care/, which becomes www.va.gov/health-care/ on Nov 7.
    * Confirmed - the robots.txt directives are for crawling, the urls published on the sitemap are accessed directly, so we'll note any robots meta tags on the pages when we go to them, but we won't have looked at the robots.txt file first.

Q: Is it possible to add a `<lastmod>` field to the sitemap at preview.va.gov/sitemap-dynamic.xml?

A: Definitely possible but might be a lift as it's not something we currently track. I'll check.

Q: Can you take down preview.va.gov/sitemap-va.xml entirely? Since it's such a mixed bag and out of spec, it's not productive.

A: Sure, will let you know when complete.

## Scope

Q: Can you confirm again that the microsites served from folders within www.va.gov will still be accessible in their current locations on and after 11/7? We want to check our understanding that we won't need to reindex these items in the near future, because they'll continue to be where they are right now.

A: Confirmed. No plans to immediately deprecate or move any of them.

Q: If we can't churn through the 100 and 200 priority groups before 11/7, what will happen? How much search traffic do you currently get that goes from the central www.va.gov search to these subdomains?

A: It's absolutely fine if those are added over time, even over the course of a few weeks. I'll review and identify any exceptions but for now assume they can all be crawled at convenience. The most trafficked facility sites, for example, get ~15k unique hits per week, but very few are sent from internal search.
