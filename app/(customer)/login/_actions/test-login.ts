"use server"

import { Role } from "@prisma/client"
import { createHash, randomBytes, timingSafeEqual } from "node:crypto"
import { cookies } from "next/headers"
import { redirect } from "next/navigation"
import { db } from "@/app/_lib/prisma"

const VALIDADE_DA_SESSAO_SEGUNDOS = 60 * 60 * 24 * 30

const loginDeTesteAtivado = () => process.env.TEST_LOGIN_ENABLED === "true"

const senhaConfere = (senha: string) => {
  const esperada = process.env.TEST_LOGIN_PASSWORD?.trim()
  if (!esperada) return false

  const recebida = createHash("sha256").update(senha).digest()
  const alvo = createHash("sha256").update(esperada).digest()
  return timingSafeEqual(recebida, alvo)
}

// Login somente para testes: cria uma sessão de banco no formato que o
// NextAuth (estratégia "database") já lê, sem depender do OAuth do Google.
// Fica inerte quando TEST_LOGIN_ENABLED não é "true".
export const testLogin = async (formData: FormData) => {
  if (!loginDeTesteAtivado()) {
    redirect("/")
  }

  const email = String(formData.get("email") ?? "")
    .trim()
    .toLowerCase()
  const senha = String(formData.get("password") ?? "")

  if (!email || !senhaConfere(senha)) {
    redirect("/login?erro=credenciais")
  }

  const user = await db.user.findUnique({
    where: { email },
    select: { id: true, role: true },
  })

  if (!user) {
    redirect("/login?erro=credenciais")
  }

  const sessionToken = randomBytes(32).toString("hex")
  await db.session.create({
    data: {
      sessionToken,
      userId: user.id,
      expires: new Date(Date.now() + VALIDADE_DA_SESSAO_SEGUNDOS * 1000),
    },
  })

  const useSecureCookies = (process.env.NEXTAUTH_URL ?? "").startsWith(
    "https://",
  )

  const cookieStore = await cookies()
  cookieStore.set(
    `${useSecureCookies ? "__Secure-" : ""}next-auth.session-token`,
    sessionToken,
    {
      httpOnly: true,
      sameSite: "lax",
      path: "/",
      secure: useSecureCookies,
      maxAge: VALIDADE_DA_SESSAO_SEGUNDOS,
    },
  )

  redirect(user.role === Role.BARBER_ADMIN ? "/dashboard" : "/bookings")
}
