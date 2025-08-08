

class HttpStatusConstant:
    """
    返回状态码

    SUCCESS: 操作成功
    CREATED: 对象创建成功
    ACCEPTED: 请求已经被接受
    NO_CONTENT: 操作已经执行成功，但是没有返回数据
    MOVED_PERM: 资源已被移除
    SEE_OTHER: 重定向
    NOT_MODIFIED: 资源没有被修改
    BAD_REQUEST: 参数列表错误（缺少，格式不匹配）
    UNAUTHORIZED: 未授权
    FORBIDDEN: 访问受限，授权过期
    NOT_FOUND: 资源，服务未找到
    BAD_METHOD: 不允许的http方法
    CONFLICT: 资源冲突，或者资源被锁
    UNSUPPORTED_TYPE: 不支持的数据，媒体类型
    ERROR: 系统内部错误
    NOT_IMPLEMENTED: 接口未实现
    WARN: 系统警告消息
    """

    SUCCESS = 200
    CREATED = 201
    ACCEPTED = 202
    NO_CONTENT = 204
    MOVED_PERM = 301
    SEE_OTHER = 303
    NOT_MODIFIED = 304
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    BAD_METHOD = 405
    CONFLICT = 409
    UNSUPPORTED_TYPE = 415
    ERROR = 500
    NOT_IMPLEMENTED = 501
    WARN = 601


class CommonConstant:
    """
    常用常量

    WWW: www主域
    HTTP: http请求
    HTTPS: https请求
    LOOKUP_RMI: RMI远程方法调用
    LOOKUP_LDAP: LDAP远程方法调用
    LOOKUP_LDAPS: LDAPS远程方法调用
    YES: 是否为系统默认（是）
    NO: 是否为系统默认（否）
    DEPT_NORMAL: 部门正常状态
    DEPT_DISABLE: 部门停用状态
    UNIQUE: 校验是否唯一的返回标识（是）
    NOT_UNIQUE: 校验是否唯一的返回标识（否）
    """

    WWW = 'www.'
    HTTP = 'http://'
    HTTPS = 'https://'
    LOOKUP_RMI = 'rmi:'
    LOOKUP_LDAP = 'ldap:'
    LOOKUP_LDAPS = 'ldaps:'
    YES = 'Y'
    NO = 'N'
    DEPT_NORMAL = '0'
    DEPT_DISABLE = '1'
    UNIQUE = True
    NOT_UNIQUE = False


