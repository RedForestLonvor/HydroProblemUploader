# [USACO2001]笔直的水管

## Description

奶牛们想把水从池塘运输到牛棚里，池塘和牛棚相距$D$个单位.它们有P根水管，每根水管由2个整数来描述：水管长度$L_i$，最大流量％.
水管可以依次连接构成一条运输管道，那么这条运输管道的流量就是构成这条管道的所有水管中最小的一个流量. 但是，要让水从池塘通过运输管道流到牛棚里，管道的长度必须恰好等于池塘和牛棚的距离.（<span style="color:rgb(85,86,102);">也就是说，水管长度$L_i$之和为$D$</span>)
现在只要求构造一条运输管道，求其最大流量.


## Sample Input 1

```
7 6
45
36
27
14
67
15
```

## Sample Output 1

```
5
```

