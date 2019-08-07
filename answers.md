### 2.

I estimate I've spent somewhere around 12 hours in total on the coding assignment,
but a very large part of that was caused by three things:

- I hadn't used Zappa or AWS Lambda before, and took this opportunity to learn more about those.
  Using my preferred stack for side projects (Docker Swarm on some sort of VPS) would have been
  much faster due to familiarity.
- I hit a strange issue in Vuex where store properties were not properly becoming reactive.
  In the end I solved this problem by using a factory function for the state like one would do with
  Redux. However, diagnosing the issue took a long time - I have been playing with Vue for about 2 years
  at this point and never had encountered anything like this before.
  Without these two roadbumps, I think it would have take approximately 6-7 hours.

If I had more time, there are a few improvements I'd like to make:

**Frontend**

- Proper pagination for the things view
- Along the same lines, more extensive filtering capabilities
- Some sort of UI/E2E testing
- A different library for the JSON editor - this one works but throws a bunch
  of errors

**Both**

- I thought for a while about implementing an _enum_ data type for the metadata field,
  but had trouble thinking of an time-efficient way of getting it to work. There would need to
  be a way of defining these enums beforehand, and some sort of way to make a distinction between
  enum values and plain strings. This means that the current light-weight approach of just using
  JSON wouldn't cut it anymore. For now I have found that using JSON is a good 80/20 compromise for the
  problem of storing structured metadata.
- I would probably have tried to use TypeScript and MyPy, although I remember typing Django didn't
  work very well last time I attempted it.

**Backend**

- I would have used a different library for the audit log, or implemented it myself. This one mostly
  works, but creates superfluous models and conflicts with Django's built-in JSONField. However, by the time
  I discovered that, I had already spent a while building a frontend around it.

### 3.

I'm choosing to answer this question for Python. Although 3.7 is not technically the latest version,
it is the latest one I have used in anger. From that one, my favorite feature is most definitely **dataclasses**.
Where I would have most likely just used dictionaries before, dataclasses allow you to model your domain with types
in an extremely lightweight manner (compared to e.g. Java), which your IDE/editor can use to aid with linting.
What's even better is that the type metadata is available at runtime, so coupled with libraries like PyDantic
this can be used for runtime data validation in pure Python without learning any new API!

Here's an exerpt showing dataclass usage from CVGen, the library I've built to generate my CV from a YAML file:

```python
# *snip*

@dataclass
class Project:
    title: str
    description: str
    link: Optional[UrlStr]


@dataclass
class Skill:
    category: str
    keywords: List[str]


@dataclass
class CV:
    name: str
    blurb: str
    personalia: Personalia
    experience: List[Job]
    education: List[Education]
    skills: List[Skill]
    projects: List[Project]
    activities: List[Activity]
```

### 4.

Debugging backend performance issues in production can be tricky! I've definitely had to do this before.
Presumably there is some sort of logging and monitoring setup which I would use to look for clues.
Things to pay attention to:

- Resource usage graphs for individual services as well as the servers as a whole (if they are shared).
  Look for any strange patterns, such as spikes, cliffs, anything that jumps out
- Status code charts - is there some uptick in 400/500 range codes?
- Response times - are the servers slowed down by some particularly pathological requests?
- Errors, timeouts or similar in the logs. If any external services are in use on the critical path, are these
  still up and healthy?

If nothing jumps out immediately, I would proceed to track down the start time of the performance issues, and check
in version control, and see if any suspicious patterns
are present in the code that has been deployed lately. Are there some O(n^2) algorithms being used anywhere?

In my personal experience, the culprit is often related to database/datastore access.
So I would also pay attention to N+1 patterns, missing indices, full table scans (EXPLAIN is your friend) and
other such things. Hopefully I can get my hands on an anonymized database dump that I can use to try and reproduce the issues locally.

If the performance problems are in the frontend, I'd additionally look into inefficient network calls (using many individual GETs instead of a LIST endpoint),
DOM transforms in tight loops, improperly compressed static assets.
