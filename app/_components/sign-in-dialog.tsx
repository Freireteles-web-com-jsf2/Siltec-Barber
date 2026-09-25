"use client"

import { signIn } from "next-auth/react"
import { Button } from "./ui/button"
import Image from "next/image"

// Ação de login com o Google. Renderizado na página /login (é o único ponto
// da interface que dispara o OAuth), por isso não abre dialog: navega direto.
const SignInDialog = () => {
  const handleLoginWithGoogleClick = () => {
    const callbackUrl =
      new URLSearchParams(window.location.search).get("callbackUrl") ?? "/"

    signIn("google", { callbackUrl })
  }

  return (
    <Button
      variant="outline"
      className="w-full gap-1 font-bold"
      onClick={handleLoginWithGoogleClick}
      type="button"
    >
      <Image
        alt="Fazer login com o Google"
        src="/google.svg"
        width={18}
        height={18}
      />
      Entrar com Google
    </Button>
  )
}

export default SignInDialog
