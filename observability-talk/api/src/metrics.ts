import {
  collectDefaultMetrics,
  Registry,
  Histogram,
  Counter,
} from "prom-client";
import express, { Request, Response, NextFunction } from "express";

const register = new Registry();
collectDefaultMetrics({ register });

const httpRequestDuration = new Histogram({
  name: "http_request_duration_seconds",
  help: "Duration of HTTP requests in seconds",
  labelNames: ["method", "route", "status_code"],
  registers: [register],
});

const httpRequestCount = new Counter({
  name: "http_request_count",
  help: "Total number of HTTP requests",
  labelNames: ["method", "route", "status_code"],
  registers: [register],
});

const metricsMiddleware = (req: Request, res: Response, next: NextFunction) => {
  const end = httpRequestDuration.startTimer();
  res.on("finish", () => {
    const labels = {
      method: req.method,
      route: req.route?.path || req.path,
      status_code: res.statusCode,
    };
    end(labels);
    httpRequestCount.inc(labels);
  });
  next();
};

const metricsRouter = express.Router();
metricsRouter.get("/metrics", async (req: Request, res: Response) => {
  res.set("Content-Type", register.contentType);
  res.end(await register.metrics());
});

export {
  register,
  httpRequestDuration,
  httpRequestCount,
  metricsMiddleware,
  metricsRouter,
};
