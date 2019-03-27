# The Missing Link
Given two sets of entities - a sample group and a control group - identify
relationships the sample entities have in common with each other but not
with the control group.

For example, given ...

* A sample set of IP addresses exhibiting malicious behavior and assumed to be infected with malware
* A control group of IPs assumed (but not known) to be clean
* A list of network connections made by both groups

... determine what network traffic the infected IPs have in common with
each other but not in common with the control group.  This raises the botnet
control channel to the top of the list while minimizing traffic that all
hosts have in common such as social media and content delivery networks.

For each relationship target, the algorithm outputs these fields:

* target - the target of the relationship (e.g. destination IP)
* ratio - the ratio of related sample entities to related control entities.  A ratio > 1 means the target is over represented in the sample group.  A ratio == 1 means the target is equally represented in both groups.  A ratio < 1 means the target is underrepresented in the sample group.
* deviations_from_mean - the number of standard deviations from the average ratio
* sample_count - the number of entities in the sample group with this relationship
* sample_percent - the percent of entities in the sample group with this relationship
* control_count - the number of entities in the control group with this relationship
* control_percent - the percent of entities in the control group with this relationship

Note: if labels are provided for the two sets when the object is
instantiated, those labels will be used instead of "sample" and "control."
