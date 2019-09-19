# kube-into
first commit




input {
  beats {
    port => "5044"
  }
}
filter {
ruby {
    code => "
            project = event.get('source').split('/')
            project.each do |temp2|
                if temp2.nil? then
                    next
                end
                key = 'project'
                value = project[-2]
                if key.nil? then
                    next
                end
                event.set(key, value)
            end
             if  project[-2] == 'nginx-ingress-controller' then
                     event.set('request_data_tokenId', event.get('[json][log]'))
               end
            if  project[-2] == 'pp-reconciliation-dist' then
                     event.set('request_data_tokenId', event.get('[json][log]'))
               end
    "
}
if 'nginx-ingress-controller' in [project]{
json{
        source => "request_data_tokenId"
    }
    mutate {
        remove_field => ["json","request_data_tokenId"]
    }
}
if 'pp-reconciliation-dist' in [project]{
json{
        source => "request_data_tokenId"
    }
}
}
output {
        elasticsearch {
        hosts => ["elasticsearch-logging:9200"]
        index => "%{project}-%{+YYYY.MM}"
        document_type => "_doc"
        }
}