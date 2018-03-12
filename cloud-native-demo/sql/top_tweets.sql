select t1.tweet_count, substr(t1.tweet_text,1,80) as tweet_text, sum(t2.followers_count) as total_reach
from (select distinct tweet_text, count(1) as tweet_count
        from tweets
        group by 1
        order by 2 desc
        limit 1) t1
inner join tweets t2
on (t1.tweet_text = t2.tweet_text)
group by 1,2;
