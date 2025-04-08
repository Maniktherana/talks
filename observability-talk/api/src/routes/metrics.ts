import { Router, Request, Response } from "express";
import { register, httpRequestDuration } from "../metrics";

const router = Router();

router.get("/custom", (req: Request, res: Response) => {
  const end = httpRequestDuration.startTimer();
  res.send("Custom metric recorded");
  end({ route: "/metrics/custom", status_code: 200, method: "GET" });
});

router.get("/metrics", async (req: Request, res: Response) => {
  res.set("Content-Type", register.contentType);
  res.end(await register.metrics());
});

export default router;
