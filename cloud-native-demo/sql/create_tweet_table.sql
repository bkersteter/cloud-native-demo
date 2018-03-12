CREATE TABLE IF NOT EXISTS tweets (
	user_id  VARCHAR(20),
        created_at TIMESTAMP,
        followers_count NUMERIC,
        location VARCHAR(1000),
        favorite_count NUMERIC,
        retweet_count NUMERIC,
        tweet_text  VARCHAR(1000)
);
