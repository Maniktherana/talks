import express from "express";
import { Request, Response } from "express";

import { metricsMiddleware, metricsRouter } from "./metrics";
import { metrics } from "@opentelemetry/api";

import { createLogger, format, transports } from "winston";
import LokiTransport from "winston-loki";

const app = express();

const logger = createLogger({
  level: "info",
  format: format.combine(format.timestamp(), format.json()),
  transports: [
    new transports.Console(),
    new LokiTransport({
      host: "http://loki:3100",
      labels: { job: "express-api" },
      json: true,
      onConnectionError: (err: any) =>
        console.error("Loki connection error:", err),
    }),
  ],
});

app.use(metricsMiddleware);
app.use(express.json());

app.use(metricsRouter);

// Middleware to collect metrics
app.use((req, res, next) => {
  const meter = metrics.getMeter("express-server");

  // Example: Counter for total requests to any route
  const totalRequestsCounter = meter.createCounter("total_requests");
  totalRequestsCounter.add(1);

  next();
});

app.get("/", (req: Request, res: Response) => {
  logger.info("hello world");
  res.send("Hello, World!");
});

app.get("/latency/fast", (req: Request, res: Response) => {
  logger.info("fast response");
  const meter = metrics.getMeter("express-server");
  const fastLatencyCounter = meter.createCounter("latency_fast_requests");
  fastLatencyCounter.add(1);
  res.send("Fast response");
});

app.get("/latency/medium", (req: Request, res: Response) => {
  const latency = Math.floor(Math.random() * (2000 - 500 + 1)) + 500;
  setTimeout(() => {
    logger.info("medium response");
    const meter = metrics.getMeter("express-server");
    const mediumLatencyCounter = meter.createCounter("latency_medium_requests");
    mediumLatencyCounter.add(1);
    res.send("Medium response");
  }, latency);
});

app.get("/latency/slow", (req: Request, res: Response) => {
  const latency = Math.floor(Math.random() * (10000 - 4000 + 1)) + 4000;
  setTimeout(() => {
    logger.info("slow response");
    const meter = metrics.getMeter("express-server");
    const slowLatencyCounter = meter.createCounter("latency_slow_requests");
    slowLatencyCounter.add(1);
    res.send("Slow response");
  }, latency);
});

app.get("/logs/info", (req: Request, res: Response) => {
  logger.info("This is an info log");
  res.send("Info log recorded");
});

app.get("/logs/warn", (req: Request, res: Response) => {
  logger.warn("This is a warning log");
  res.send("Warning log recorded");
});

app.get("/logs/error", (req: Request, res: Response) => {
  logger.error("This is an error log");
  res.send("Error log recorded");
});

const PORT = process.env.PORT || 5050;
app.listen(PORT, () => {
  logger.info(`Server is running on port ${PORT}`);
});

export default app;
