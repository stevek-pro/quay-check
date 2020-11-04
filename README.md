# CLI Tool to check docker build states

```bash
usage: quay [-h] -t TAG [-r SAVEUP-EXAMPLE]

Script for verifing the presence of Docker builds for certain tags in Quay.

optional arguments:
  -h, --help            show this help message and exit
  -r SAVEUP-EXAMPLE, --repo SAVEUP-EXAMPLE
                        Limit lookup to one repository
  -e repo1,repo2        Exclude specified repositores

required arguments:
  -t TAG, --tag TAG     Lookup for certain build tag
```

## Example run

```bash
~ # quay -t develop -r saveup-policy-front

Service: saveup-policy-front
	Build Start			Tags		Phase
	Mon, 26 Mar 2018 15:15:04 -0000	develop, latest error
	Mon, 26 Mar 2018 13:12:35 -0000	develop, latest expired
	Thu, 22 Mar 2018 09:13:33 -0000	develop, latest complete
	Wed, 21 Mar 2018 18:23:22 -0000	develop, latest error
	Wed, 21 Mar 2018 17:10:53 -0000	develop, latest error
	Wed, 21 Mar 2018 15:17:50 -0000	develop, latest error
	Wed, 21 Mar 2018 14:43:10 -0000	develop, latest complete
	Wed, 21 Mar 2018 11:20:57 -0000	develop, latest complete
	Wed, 21 Mar 2018 11:20:27 -0000	develop, latest complete
	Tue, 20 Mar 2018 18:55:45 -0000	develop, latest complete
	Tue, 20 Mar 2018 18:21:21 -0000	develop, latest complete
	Tue, 20 Mar 2018 13:30:52 -0000	develop, latest complete
	Tue, 20 Mar 2018 12:30:33 -0000	develop, latest error
	Tue, 20 Mar 2018 10:37:13 -0000	develop, latest error

```