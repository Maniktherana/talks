<img width="1149" alt="Screenshot 2024-06-22 at 11 41 05 PM" src="https://github.com/Maniktherana/observability-talk/assets/14011425/80981bcf-11e3-4072-99c7-8b25fb249b18">

# Intro to Observability

In this talk I give a brief introduction to observability, what it is, why it is important, and how to get started with it. I also discuss the differences between observability and monitoring, and how they can be used together to improve the reliability and performance of your systems.

This talk also has a demo where I show how to use Prometheus, Loki and Grafana to monitor a simple web server.

## How to run

To run the demo, you will need to have Docker and Docker Compose installed on your machine. You can then run the following command:

```bash
docker compose up
```

This will start a simple web server, Prometheus, Loki and Grafana. You can then access the web server at `http://localhost:5050`, Prometheus at `http://localhost:9090`, and Grafana at `http://localhost:3000`. Grafana is already configured to use Prometheus and Loki as a data source, and has a dashboard that shows relevant data from both sources.

You can use ping_endpoints1.sh and ping_endpoints2.sh to generate traffic to the web server, allowing you to see the metrics in Prometheus and the logs in both Loki and Grafana.
