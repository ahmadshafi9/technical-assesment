import { tool } from "ai";
import { z } from "zod";
import { spawnSync } from "child_process";

export const analyzeTool = tool({
  description:
    "Execute Python code for data analysis, calculations, or processing. The LLM writes Python code, and this tool runs it and returns the output.",
  parameters: z.object({
    code: z.string().describe("The Python code to execute"),
  }),
  execute: async (params) => {
    try {
      const result = spawnSync("python3", ["-c", params.code], {
        timeout: 10000, // 10 seconds
        encoding: "utf-8",
        maxBuffer: 10 * 1024 * 1024, // 10MB buffer for large outputs
      });

      if (result.error) {
        return {
          error: `Failed to execute Python code: ${result.error.message}`,
          exitCode: 1,
        };
      }

      return {
        stdout: result.stdout || "",
        stderr: result.stderr || "",
        exitCode: result.status || 0,
      };
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : String(error);
      return {
        error: `Error executing Python code: ${errorMessage}`,
        exitCode: 1,
      };
    }
  },
});
