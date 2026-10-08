import "dotenv/config";
import { defineConfig } from "drizzle-kit";

// DATABASE_URL이 없으면(로컬 파일) "sqlite", Turso(libsql://...)로 옮기면 "turso" dialect를 쓴다.
// drizzle-kit은 dialect별로 dbCredentials 타입이 달라서(turso만 authToken을 받는다) 둘을 분기한다.
const url = process.env.DATABASE_URL || "file:local.db";
const authToken = process.env.DATABASE_AUTH_TOKEN;

export default defineConfig(
  authToken
    ? {
        schema: "./server/db/schema.ts",
        out: "./drizzle",
        dialect: "turso",
        dbCredentials: { url, authToken },
      }
    : {
        schema: "./server/db/schema.ts",
        out: "./drizzle",
        dialect: "sqlite",
        dbCredentials: { url },
      }
);
