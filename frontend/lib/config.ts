const projectName = process.env.NEXT_PUBLIC_PROJECT_NAME

if (!projectName) throw new Error("必须配置 NEXT_PUBLIC_PROJECT_NAME")

export { projectName }
