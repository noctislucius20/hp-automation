FROM sebp/elk
ADD 02-beats-input.conf /etc/logstash/conf.d/
ADD 12-filter.conf /etc/logstash/conf.d/
ADD 30-output.conf /etc/logstash/conf.d/
ADD elasticsearch.yml /opt/elasticsearch/config/
ADD kibana.yml /opt/kibana/config/
