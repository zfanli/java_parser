# java_parser

Python based Java parser. Parsing for analysis.

### Memo

**For some reasons, comments in some legacy asserts may be written in a strange way, like this**

```java
/*
 --------
 Comment,
 End.
 --------
*/
something;
```

It looks a little bit strange but is acceptable for human. However when try to parsing this comment, the parser cannot recognize where to end if two comment blocks are near by. Like this.

```java
/*
 --------
 Comment,
 End.
 --------
*/
something;

/*
 --------
 Some
 others.
 --------
*/
another;
```

We know that we can write any thing inside a comment block, so for parse a comment body, the regex maybe like `/\*.*/`, for match any character start with a star symbol. If there is no start symbol prefix, what will happened?

For the above code, `something;` will be parsed as comment, the result will be only `another;` and all of things above it are parsed as comments.

As a solution for this problem, maybe adding stat prefix before parsing would be a good way to resolve it?
