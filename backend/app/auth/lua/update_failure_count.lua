local success = ARGV[1] == '1'
local max_failures = tonumber(ARGV[2])
local lock_duration_seconds = tonumber(ARGV[3])
local failure_window_seconds = tonumber(ARGV[4])

local failure_count = tonumber(redis.call('GET', KEYS[1]) or '0')

if failure_count >= max_failures then
    return math.max(1, redis.call('TTL', KEYS[1]))
end

if success then
    redis.call('DEL', KEYS[1])
    return 0
end

failure_count = redis.call('INCR', KEYS[1])

if failure_count == 1 then
    redis.call('EXPIRE', KEYS[1], failure_window_seconds)
end

if failure_count == max_failures then
    redis.call('EXPIRE', KEYS[1], lock_duration_seconds)
    return lock_duration_seconds
end

return 0
