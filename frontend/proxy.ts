import { type NextRequest, NextResponse } from "next/server"

const publicPaths = new Set(["/login", "/forgot-password"])

export function proxy(request: NextRequest) {
  const { pathname } = request.nextUrl

    const hasSession = request.cookies.has("session")

  if (!hasSession && !publicPaths.has(pathname)) {
    return NextResponse.redirect(new URL("/login", request.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: ["/((?!api|_next|.*\\..*).*)"],
}
