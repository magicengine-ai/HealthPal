package main

import (
	"log"
	"net/http"
)

func main() {
	log.Println("🚀 HealthPal Backend Starting...")
	
	// 健康检查接口
	http.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("OK"))
	})
	
	// API 路由
	http.HandleFunc("/v1/auth/login", handleLogin)
	http.HandleFunc("/v1/auth/register", handleRegister)
	http.HandleFunc("/v1/user/profile", handleUserProfile)
	http.HandleFunc("/v1/records/upload", handleRecordUpload)
	http.HandleFunc("/v1/records/", handleRecord)
	http.HandleFunc("/v1/indicators/", handleIndicators)
	http.HandleFunc("/v1/medications/", handleMedications)
	
	log.Println("📡 Server listening on :8080")
	if err := http.ListenAndServe(":8080", nil); err != nil {
		log.Fatal(err)
	}
}

// 占位处理函数 - 后续实现
func handleLogin(w http.ResponseWriter, r *http.Request)     { w.Write([]byte("TODO: Login")) }
func handleRegister(w http.ResponseWriter, r *http.Request)  { w.Write([]byte("TODO: Register")) }
func handleUserProfile(w http.ResponseWriter, r *http.Request) { w.Write([]byte("TODO: Profile")) }
func handleRecordUpload(w http.ResponseWriter, r *http.Request) { w.Write([]byte("TODO: Upload")) }
func handleRecord(w http.ResponseWriter, r *http.Request)    { w.Write([]byte("TODO: Record")) }
func handleIndicators(w http.ResponseWriter, r *http.Request) { w.Write([]byte("TODO: Indicators")) }
func handleMedications(w http.ResponseWriter, r *http.Request) { w.Write([]byte("TODO: Medications")) }
