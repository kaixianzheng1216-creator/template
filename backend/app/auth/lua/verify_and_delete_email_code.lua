local stored_code_hash = redis.call('GET', KEYS[1])

if stored_code_hash == ARGV[1] then
    redis.call('DEL', KEYS[1])
    return 1
end

return 0
