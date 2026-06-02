source "https://rubygems.org"

# Pin the exact GitHub Pages build environment so a local
# `bundle exec jekyll build` renders identically to the live site — including
# jekyll-default-layout (assigns default.html to layout-less docs) and
# jekyll-seo-tag (the {% seo %} tag). This is for local testing of the layout /
# SEO output; GitHub Pages itself still builds the site from this same gem set.
gem "github-pages", group: :jekyll_plugins
gem "webrick"  # needed for `jekyll serve` on Ruby 3+
