# Open Syllabus Project REST API

This document serves as the specification for the implementation of the REST API
which the frontend, and other services, shall utilize. This document also
contains notes. Hopefully, this document will also become useful for
documentation.

This REST API shall use the [White House Web API
Standards](https://github.com/WhiteHouse/api-standards).

Remember: this is just a sloppy draft, so feel free to make suggestions, PRs,
etc.

## Terminology

  * Doc, Syllabi:
  * Title:

## Special Considerations

  * "Date or date range of classes taught?" what?
  * what do we all want to be able to filter titles by in first iteration?
  * a 'mock' parameter for mock data?
  * This is a read-only API, only GET and OPTIONS
  * Vertical scaling, general speed
  * Security, authentication
  * Do you think we'll have to worry about disambiguation for same-titles?
  * Caching; cache specific queries for re-use... but how does cache update?
  * Publisher and other discrepancies

## Technologies

The technologies I've selected for this project are:

  * Flask, flask-restful
  * Docker
  * Celery
  * Postgres: love the json features. Fast! can index by syllabi_by_field > id!
    This can help with caching reponses.
  * Travis CI
  * JSON
  * Python 3

## Resources

The Syllabi API provides six different resources:

  * Titles (books, magazines, articles, etc.)
  * Authors
  * Schools
  * Fields
  * Countries
  * Publishers

### Titles (/v1/titles)

Books, articles, things of that nature. _Not_ syllabi.

#### `GET /v1/titles/someid.json`

Request a specific title entity by ID.

Example response:

    {
        "id": "asdf0e039f2",
        "name": "Woopelty Boobelty",
        "authors": ["some author", "another author"],
        "publisher": "publisherid",
        "publish_date": 20170506,
        "description": "blah blah lorem ipsum, you know the drill",
        "syllabi_by_field": [
            {
                "id": "fieldid",
                "count": 123
            },
            {
                "id": "anotherfieldid",
                "count": 99
            }
        ],
        "rank": 1,
        "appearances": 200,
        "score": 6.5,
        "assigned_with": ["titleid", "yetanothertitleid"],
    }

#### `GET /v1/titles.json`

Use _queryargs_ to request a list of title entities:

  * offset:
  * limit:
  * desc/asc? "order=asc" or "order=desc"
  * hasopen (has open access resources)  this won't be implemented in first
    iteration?
  * publish date (last 50 years, last 10 years) "pubdate=last50" or
    "pubdate=last10?" caching bonuses there, but what if we just did
    variable date searches

Example request:

`GET /v1/titles.json?offset=10&limit=20`

Response:

    {
        "metadata": {
            "resultset": {
                "count": 123,
                "offset": 10,
                "limit": 20,
            }
        },
        "results": [
            {
                "id": "asdf0e039f2",
                "name": "Woopelty Boobelty",
                "authors": ["some author", "another author"],
                "publisher": "publisherid",
                "publish_date": 20170506,
                "description": "blah blah lorem ipsum, you know the drill",
                "syllabi_by_field": [
                    {
                        "id": "fieldid",
                        "count": 123
                    },
                    {
                        "id": "anotherfieldid",
                        "count": 99
                    }
                ],
                "rank": 1,
                "appearances": 200,
                "score": 6.5,
                "assigned_with": ["titleid", "yetanothertitleid"],
            },
            {
                "id": "asdf0e039f2",
                "name": "Woopelty Boobelty",
                "authors": ["some author", "another author"],
                "publisher": "publisherid",
                "publish_date": 20170506,
                "description": "blah blah lorem ipsum, you know the drill",
                "syllabi_by_field": [
                    {
                        "id": "fieldid",
                        "count": 123
                    },
                    {
                        "id": "anotherfieldid",
                        "count": 99
                    }
                ],
                "rank": 1,
                "appearances": 200,
                "score": 6.5,
                "assigned_with": ["titleid", "yetanothertitleid"],
            }
        ],
    }

### Authors (/v1/authors)

Authors of titles.

#### `GET /v1/authors/someid.json`

Request a specific author entity by ID.

Example response:

    {
        "id": "sumauthorid",
        "name": "Fredric Jameson",
        "description": "blah blah lorem ipsum, you know the drill",
        "appearances": 200,
        "syllabi_by_field": [
            {
                "id": "fieldid",
                "count": 123
            },
            {
                "id": "anotherfieldid",
                "count": 99
            }
        ],
        "titles": ["titleid", "yetanothertitleid"],
        "score": 9.9
    }

#### `GET /v1/authors.json`

Request authors and query for authors based these criteria, using query args:

    * Author
    * School
    * Field
    * Country
    * offset
    * limit
    * asc/desc/etc

...

### Schools (/v1/schools)

...

#### `GET /v1/schools/schoolid.json`

Request a specific school entity by ID:

    {
        "id": "someid",
        "name": "Amherst College",
        "description": "blah blah lorem ipsum, you know the drill",
        "syllabi_by_field": [
            {
                "id": "fieldid",
                "count": 123
            },
            {
                "id": "anotherfieldid",
                "count": 99
            }
        ],
        "most_assigned_titles": ["titleid", "anothertitleid"],
    }

#### `GET /v1/schools.json`

Request school entities based on these criteria, using query args:

    * School name (like match?)
    * Field 
    * Country
    * Offset
    * Limit

....

### Fields (/v1/fields)

Fields of study...

#### `GET /v1/fields.json`

Request field entities based on these criteria, using query args:

  * field (like match?)
  * country
  * offset
  * limit
  * ...

...

#### `GET /v1/fields/someid.json`

Request a specific field entity by ID.

    {
        "id": "someid",
        "name": "English",
        "top_ranked_titles": ["titleid", "anothertitleid"],
        "top_ranked_authors": ["authorid", "anotherauthorid"]
    }

### Countries (/v1/countries)

#### `GET /v1/countries/someid.json`

Request a specific country entity by ID.

Example response:

    {
        "name": "United States",
        "rank": 1,
        "syllabi": 3000000,
        "schools": 3000,
        "syllabi_by_field": [
            {
                "id": "fieldid",
                "count": 123
            },
            {
                "id": "anotherfieldid",
                "count": 99
            }
        ],
        "top_ranked_schools": ["someschoolid", "anotherschoolid"],
        "top_ranked_titles": ["sometitleid", "anothertitleid"],
        "top_ranked_authors": ["someauthorid", "anotherauthorid"]
    }

#### `GET /v1/countries.json`

Request a list of country entities which match criteria specified by these query
args:

  * limit
  * offset
  * country (like match?)
  * Field

...

### Publishers (/v1/publishers)


#### `GET /v1/publishers/someid.json`

Request a specific publisher entity by ID.

Example response:

    {
        "name": "Oxford University Press",
        "top_ranked_titles": ["titleid", "anothertitleid"],
        "top_ranked_authors": ["authorid", "anotherauthorid"]
    }

#### `GET /v1/publishers.json`

Request a list of publisher entities which match criteria specified by these query
args:

  * limit
  * offset
  * publisher (like match?)
  * field
  * country
  * published date range? (pub last 50, last 10)

...
