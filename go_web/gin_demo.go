package main

import (
	"encoding/json"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/go-redis/redis"
	"gorm.io/driver/mysql"
	"gorm.io/gorm"
	"gorm.io/gorm/logger"
)

var (
	db          *gorm.DB
	redisClient *redis.Client
)

type UserBasic struct {
	Id       int    `json:"id"`
	Username string `json:"username"`
	Role     string `json:"role"`
}

func (UserBasic) TableName() string {
	return "user_basic"
}

func initDB() *gorm.DB {
	var err error
	db, err = gorm.Open(mysql.Open("root:123456@/house_rental"), &gorm.Config{
		// 将LogMode设置为logger.Silent以禁用日志打印
		Logger: logger.Default.LogMode(logger.Silent),
	})
	if err != nil {
		panic("failed to connect database")
	}

	sqlDB, err := db.DB()

	// SetMaxIdleConns sets the maximum number of connections in the idle connection pool.
	sqlDB.SetMaxIdleConns(10)

	// SetMaxOpenConns sets the maximum number of open connections to the database.
	sqlDB.SetMaxOpenConns(30)

	// SetConnMaxLifetime sets the maximum amount of time a connection may be reused.
	sqlDB.SetConnMaxLifetime(time.Hour)

	return db
}

func initRedis() *redis.Client {
	redisClient = redis.NewClient(&redis.Options{
		Addr: "localhost:6379",
	})
	return redisClient
}

func jsonTestHandler(c *gin.Context) {
	c.JSON(200, gin.H{
		"code": 0, "message": "gin json", "data": make(map[string]any),
	})
}

func mysqlQueryHandler(c *gin.Context) {

	// 查询语句
	var user UserBasic
	db.First(&user, "username = ?", "hui")
	//fmt.Println(user)

	// 返回响应
	c.JSON(200, gin.H{
		"code":    0,
		"message": "go mysql test",
		"data":    user,
	})

}

func cacheQueryHandler(c *gin.Context) {
	// 从Redis中获取缓存
	username := "hui" // 要查询的用户名
	cachedUser, err := redisClient.Get(username).Result()
	if err == nil {
		// 缓存存在，将缓存结果返回给客户端
		var user UserBasic
		_ = json.Unmarshal([]byte(cachedUser), &user)
		c.JSON(200, gin.H{
			"code":    0,
			"message": "gin redis test",
			"data":    user,
		})
		return
	}

	// 缓存不存在，执行数据库查询
	var user UserBasic
	db.First(&user, "username = ?", username)

	// 将查询结果保存到Redis缓存
	userJSON, _ := json.Marshal(user)
	redisClient.Set(username, userJSON, time.Minute*2)

	// 返回响应
	c.JSON(200, gin.H{
		"code":    0,
		"message": "gin redis test",
		"data":    user,
	})
}

func initDao() {
	initDB()
	initRedis()
}

func main() {
	//r := gin.Default()
	r := gin.New()
	gin.SetMode(gin.ReleaseMode) // 生产模式

	initDao()

	r.GET("/http/gin/test", jsonTestHandler)

	r.GET("/http/gin/mysql/test", mysqlQueryHandler)

	r.GET("/http/gin/redis/test", cacheQueryHandler)

	r.Run("127.0.0.1:8003")
}
