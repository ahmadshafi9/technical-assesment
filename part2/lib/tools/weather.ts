import { tool } from "ai";
import { z } from "zod";

export const weatherTool = tool({
  description:
    "Get weather forecast data for a location. Use this when the user asks about weather, temperature, rain, wind, or forecasts for any location.",
  parameters: z.object({
    latitude: z.number().describe("Latitude of the location"),
    longitude: z.number().describe("Longitude of the location"),
    forecast_days: z
      .number()
      .optional()
      .default(3)
      .describe("Number of days to forecast (1-7)"),
    daily: z
      .array(z.string())
      .optional()
      .default([
        "temperature_2m_max",
        "temperature_2m_min",
        "precipitation_sum",
        "windspeed_10m_max",
      ])
      .describe(
        "Weather variables to include (e.g., temperature_2m_max, temperature_2m_min, precipitation_sum, windspeed_10m_max, weathercode)"
      ),
  }),
  execute: async (params) => {
    try {
      const baseUrl = "https://api.open-meteo.com/v1/forecast";
      const dailyParams = params.daily.join(",");

      const url = new URL(baseUrl);
      url.searchParams.append("latitude", params.latitude.toString());
      url.searchParams.append("longitude", params.longitude.toString());
      url.searchParams.append("daily", dailyParams);
      url.searchParams.append("timezone", "auto");
      url.searchParams.append(
        "forecast_days",
        Math.min(Math.max(params.forecast_days, 1), 7).toString()
      );

      const response = await fetch(url.toString());

      if (!response.ok) {
        return {
          error: `API request failed with status ${response.status}`,
        };
      }

      const data = await response.json();

      return {
        success: true,
        data: data,
      };
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : String(error);
      return {
        error: `Failed to fetch weather data: ${errorMessage}`,
      };
    }
  },
});
