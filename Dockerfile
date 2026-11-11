FROM mcr.microsoft.com/dotnet/sdk:10.0 AS build
WORKDIR /src
COPY src/9circ.Core/9circ.Core.csproj src/9circ.Core/
COPY src/9circ.Api/9circ.Api.csproj src/9circ.Api/
RUN dotnet restore src/9circ.Api/9circ.Api.csproj
COPY . .
RUN dotnet publish src/9circ.Api/9circ.Api.csproj -c Release -o /app/publish --no-restore

FROM mcr.microsoft.com/dotnet/aspnet:10.0 AS runtime
WORKDIR /app
COPY --from=build /app/publish .
ENV ASPNETCORE_URLS=http://+:8080
EXPOSE 8080
USER $APP_UID
ENTRYPOINT ["dotnet", "9circ.Api.dll"]
