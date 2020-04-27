This file describes exact behavior of methods for different edge cases and 
explains general logic. This description covers the behavior of get_tld, 
get_tld_unsafe, get_sld, get_sld_unsafe, split_domain, split_domain_unsafe

1. general difference of get_*() and get_*_unsafe() methods:
get_*_unsafe() does not perform if the input string is None and does not 
transforms it to the lower case.

2. The listed above methods works only with non-canonical FQDN strings - 
trailing dot must be removed before call the method. This restriction allows 
get rid of fuzzy logic in edge cases.

3. DNS does not support empty labels - if some label detected to be empty, 
None will be returned. 

4. Every method processes provided FQDN in the reverse order, from the last 
label towards the start of the string. It stops when the specific task is 
completed. Therefore no validation occurs outside of this scope.  For example,
```
get_tld('......com') -> 'com'
``` 
as leading dots are not processed.
split_domain method is based on get_sld method - it returns everything in 
front of get_sld() as a prefix.
Specifically to example above 
```
split_domain('......com') -> ('....',None,'com')
```
Edge cases and expected behavior
The behavior of the library can be illustrated best on the small examples:
(boolean arguments are omitted if does not affect behavior )

## get_tld()
###Degenerate case (empty list)

| input  | strict  | wildcard | result | notes |
|--------|---------|----------|--------|-------|
| ''     |         |          | None   | empty labels are not allowed |
| '.'    |         |          | None   | empty labels are not allowed |
| '..'   |         |          | None   | empty labels are not allowed |
| '....' |         |          | None   | empty labels are not allowed |
| 'abc'  | false   |          | 'abc'  | non-strict mode, the last label is TLD |
| 'abc'  | true    |          | None   | 'abc' not in the list |
| '.abc' | false   |          | 'abc'  | non-strict mode, the last label is TLD |
| '.abc' | true    |          | None   | 'abc' not in the list |
| 'abc.' |         |          | None   | empty labels are not allowed |
| '....abc' | false |         | 'abc'  | non-strict mode, string head is not processed|
| '....abc' | true  |         | None   | 'abc' not in the list |
| 'example.abc' | false |     | 'abc'  | non-strict mode, the last label is TLD |
| 'example.abc' | true  |     | None   | 'abc' not in the list |

###Simple case, no wildcards (['com'])

| input  | strict  | wildcard | result | notes |
|--------|---------|----------|--------|-------|
| ''     |         |          | None   | empty labels are not allowed |
| '.'    |         |          | None   | empty labels are not allowed |
| '..'   |         |          | None   | empty labels are not allowed |
| '....' |         |          | None   | empty labels are not allowed |
| 'abc'  | false   |          | 'abc'  | non-strict mode |
| 'abc'  | true    |          | None   | not in the list |
| 'com'  |         |          | 'com'  | allowed TLD |
| '.abc' | false   |          | 'abc'  | non-strict mode |
| '.abc' | true    |          | None   | not in the list |
| '.com' |         |          | 'com'  | allowed TLD |
| 'abc.' |         |          | None   | empty labels are not allowed |
| '....abc' | false  |        | 'abc'  | non-strict mode, string head is not processed|
| '....abc' | true   |        | None   | not in the list |
| '....com' |   |        | 'com'  | allowed TLD, string head is not processed|
| 'example.abc' | false |     | 'abc'  | non-strict mode, the last label is TLD |
| 'example.abc' | true  |     | None   | 'abc' not in the list |
| 'example.com' |  |     | 'com'  | allowed TDL |

### Simple case, negation, no wildcards (['com', '!org'])

| input  | strict  | wildcard | result | notes |
|--------|---------|----------|--------|-------|
| ''     |         |          | None   | empty labels are not allowed |
| '.'    |         |          | None   | empty labels are not allowed |
| '..'   |         |          | None   | empty labels are not allowed |
| '....' |         |          | None   | empty labels are not allowed |
| 'abc'  | false   |          | 'abc'  | non-strict mode |
| 'abc'  | true    |          | None   | not in the list |
| 'com'  |         |          | 'com'  | allowed TLD |
| 'org'  |         |          | None   | not allowed TLD |
| '.abc' | false   |          | 'abc'  | non-strict mode |
| '.abc' | true    |          | None   | not in the list |
| '.com' |         |          | 'com'  | allowed TLD |
| '.org' |         |          | None   | not allowed TLD |
| 'abc.' |         |          | None   | empty labels are not allowed |
| 'com.' |         |          | None   | empty labels are not allowed |
| 'org.' |         |          | None   | empty labels are not allowed |
| '....abc' | false  |        | 'abc'  | non-strict mode, string head is not processed|
| '....abc' | true   |        | None   | not in the list |
| '....com' |   |        | 'com'  | allowed TLD, string head is not processed|
| '....org' |   |        | None  | not allowed TLD|
| 'example.abc' | false |     | 'abc'  | non-strict mode, the last label is TLD |
| 'example.abc' | true  |     | None   | 'abc' not in the list |
| 'example.com' |  |     | 'com'  | allowed TDL |
| 'example.org' |  |     | None  | not allowed TDL |
