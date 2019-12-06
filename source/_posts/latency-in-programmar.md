---
layout: poster
title: latency-in-programmar
date: 2019-02-11 19:47:46
tags: [tips]
---
<!-- TOC -->

- [Latency Comparison Numbers (~2012)](#latency-comparison-numbers-2012)
    - [Notes](#notes)
    - [Credit](#credit)
    - [Contributions](#contributions)

<!-- /TOC -->
# Latency Comparison Numbers (~2012)



<!--more-->
| **Name**                           |             |    |         |    |     |    |                             |
| ---                                | ---         | --- | ---    | --- | --- | --- | ---                       |
| L1 cache reference                 | 0.5         | ns |         |    |     |    |                             |
| Branch mispredict                  | 5           | ns |         |    |     |    |                             |
| L2 cachereference                  | 7           | ns |         |    |     |    | 14x L1 cache                |
| Mutex lock/unlock                  | 25          | ns |         |    |     |    |                             |
| Main memory reference              | 100         | ns |         |    |     |    | 20x L2 cache, 200x L1 cache |
| Compress 1K bytes with Zippy       | 3,000       | ns | 3       | us |     |    |                             |
| Send 1K bytes over 1 Gb ps network | 10,000      | ns | 10      | us |     |    |                             |
| Read 4K randomly from SSD          | 150,000     | ns | 150     | us |     |    | ~1GB/sec SSD                |
| Read 1 MB sequentially from memory | 250,000     | ns | 250     | us |     |    |                             |
| Round trip within same datacenter  | 500,000     | ns | 500     | us |     |    |                             |
| Read 1 MB sequentially from SSD    | 1,000,000   | ns | 1,000   | us | 1   | ms | ~1GB/sec SSD, 4X memory     |
| Disk seek                          | 10,000,000  | ns | 10,000  | us | 10  | ms | 20x datacenter roundtrip    |
| Read 1 MB sequentially             | 20,000,000  | ns | 20,000  | us | 20  | ms | 80x memory, 20X SSD         |
| Send pack et CA->Netherlands->CA   | 150,000,000 | ns | 150,000 | us | 150 | ms |                             |


## Notes

1 ns = 10^-9 seconds

1 us = 10^-6 seconds = 1,000 ns

1 ms = 10^-3 seconds = 1,000 us = 1,000,000 ns

## Credit

By Jeff Dean:               http://research.google.com/people/jeff/

Originally by Peter Norvig: http://norvig.com/21-days.html#answers

## Contributions

Original: https://gist.github.com/jboner/2841832

‘Humanized’ comparison:  https://gist.github.com/hellerbarde/2843375

Visual comparison chart: http://i.imgur.com/k0t1e.png