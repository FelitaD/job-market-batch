workspace {

    model {
        user = person "Job seeker" "Student in data engineering"

        system = softwareSystem "job-market-batch" "Data engineering pipeline" {

            orchestrator = container "Airflow"

            database = container "job_market" "Postgres OLAP database" {

                raw_jobs = component "raw_jobs" "Table for freshly scraped data"
                pivotted_jobs = component "pivotted_jobs" "Table for processed data"
            }

            crawler = container "data-job-crawler" "Python package for scraping job postings using Scrapy" {

                WttjLinksSpider = component "WttjLinksSpider" "Scrapes Javascript pages"
                WttjSpider = component "WttjSpider"
                wttj_links = component "wttj_links" "Text file containing a list of job postings urls"

                SpotifyLinksSpider = component "SpotifyLinksSpider" "Scrapes Javascript pages"
                SpotifySpider = component "SpotifySpider"
                spotify_links = component "spotify_links" "Text file containing a list of job postings urls"

                JobsCrawlerPipeline = component "JobsCrawlerPipeline" "Pipeline designed to insert scraped fields into local database"
            }

            etl = container "data-job-etl" "Python package for processing data" {

                transformer = component "Transformer" "TO REFACTOR"
                loader = component "Loader"
            }

            websites = container "websites" "Websites publishing job postings" {

                wttj = component "Welcome To The Jungle" "welcometothejungle.com"
                spotify = component "Spotify" "lifeatspotify.com/jobs"
            }
        }

        user -> system "Builds & Uses"

        orchestrator -> crawler "Orchestrates"
        orchestrator -> etl "Orchestrates"

        crawler -> websites "Scrapes from"
        crawler -> database "Writes to"

        etl -> database "Reads from and writes to"

        WttjLinksSpider -> wttj_links "Writes to"
        WttjSpider -> wttj_links "Reads from"
        WttjSpider -> JobsCrawlerPipeline

        SpotifyLinksSpider -> spotify_links "Writes to"
        SpotifySpider -> spotify_links "Reads from"
        SpotifySpider -> JobsCrawlerPipeline

        JobsCrawlerPipeline -> raw_jobs "Writes to"
    }

    views {
        systemContext system "SystemContext" {
            include *
            autoLayout
        }
        container system "ContainerView" {
            include *
            autoLayout
        }
        component crawler "CrawlerView" {
            include *
            autoLayout
        }
        component etl "EtlView" {
            include *
            autoLayout
        }
        component websites "WebsitesView" {
            include *
            autoLayout
        }

        styles {
            element "Software System" {
                background #1168bd
                color #ffffff
            }
            element "Person" {
                shape person
                background #08427b
                color #ffffff
            }
        }
    }
}