import { PrismaNeonHttp } from "@prisma/adapter-neon"
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

  if (!/^postgres(ql)?:\/\//.test(connectionString)) {
    throw new Error(
      "DATABASE_URL must be a PostgreSQL URL, for example postgresql://user:pass@host:5432/db.",
    )
  }

  return connectionString
}

function createPrismaClient(): PrismaClient {
  // Adapter HTTP do Neon: usa fetch nativo (sem WebSocket/`ws`), adequado a
  // serverless. O `$transaction` em batch usado no app é suportado por ele.
  const adapter = new PrismaNeonHttp(getDatabaseUrl(), {})
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
