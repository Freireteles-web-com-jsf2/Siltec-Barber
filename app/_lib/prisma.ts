import { PrismaBetterSqlite3 } from "@prisma/adapter-better-sqlite3"
import { PrismaClient } from "@prisma/client"

declare global {
  // eslint-disable-next-line no-unused-vars
  var cachedPrisma: PrismaClient | undefined
}

function getDatabaseUrl(): string {
  const connectionString = process.env.DATABASE_URL?.trim()

  if (!connectionString) {
    throw new Error(
      "DATABASE_URL is not set. Please check your .env.local file.",
    )
  }

  if (!connectionString.startsWith("file:")) {
    throw new Error(
      "DATABASE_URL must be a SQLite file URL, for example file:./prisma/dev.db.",
    )
  }

  return connectionString
}

function createPrismaClient(): PrismaClient {
  const adapter = new PrismaBetterSqlite3({ url: getDatabaseUrl() })
  return new PrismaClient({ adapter })
}

export const getPrisma = (): PrismaClient => {
  if (!globalThis.cachedPrisma) {
    globalThis.cachedPrisma = createPrismaClient()
  }
  return globalThis.cachedPrisma
}

export const db = new Proxy({} as PrismaClient, {
  get(target, prop) {
    return (getPrisma() as any)[prop]
  },
})
