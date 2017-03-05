module.exports = {
    getActiveClients : function(xtrecent, ticksSinceBoot) {
        // xtrecent: content of iptables xtrecent module log
        // ticksSinceBoot: cpu ticks since boot

        result = [];

        xtrecent.split("\n").forEach(function (line)
        {
            if (line.trim() == "")
                return result;

            ip = line.substring(4, line.indexOf(" "));
            lastSeen = -1;
            split = line.split(" ")
            for (var i=0; i<split.length; i++) {
                if (split[i] == "last_seen:") {
                    ticks = parseFloat(split[i+1]);
                    lastSeen = (ticksSinceBoot - ticks) / 100;
                    lastSeen = lastSeen.toFixed(0);
                    break;
                }
            }
            if (lastSeen >= 0 && lastSeen < 3600) {
                entry = {'ip': ip, 'lastSeen': lastSeen};
                result.push(entry);
            }
        });
        return result;
    }
}
