---
name: angular-migration
description: "精通 AngularJS 到 Angular 的迁移,包括混合应用、组件转换、依赖注入变更和路由迁移。"
risk: critical
source: community
date_added: "2026-02-27"
---

# Angular 迁移

精通 AngularJS 到 Angular 的迁移,包括混合应用、组件转换、依赖注入变更和路由迁移。

## 在以下情况使用本技能

- 将 AngularJS(1.x)应用迁移到 Angular(2+)
- 运行 AngularJS/Angular 混合应用
- 将指令(directive)转换为组件(component)
- 对依赖注入进行现代化改造
- 迁移路由系统
- 更新到最新的 Angular 版本
- 实施 Angular 最佳实践

## 以下情况不要使用本技能

- 你并非在从 AngularJS 迁移到 Angular
- 应用已经在使用现代化的 Angular 版本
- 你只需要一个不涉及框架变更的小型 UI 修复

## 操作指引

1. 评估 AngularJS 代码库、依赖关系和迁移风险。
2. 选择一种迁移策略(混合方式 vs 重写)并定义里程碑。
3. 搭建 ngUpgrade,并迁移模块、组件和路由。
4. 通过测试进行验证,并规划一次安全的切换(cutover)。

## 安全性

- 避免在没有回滚方案和预发布验证的情况下进行"大爆炸式"一次性切换。
- 在增量迁移期间持续进行混合兼容性测试。

## 迁移策略

### 1. 大爆炸式(完全重写)
- 将整个应用用 Angular 重写
- 并行开发
- 一次性切换
- **最适合:** 小型应用、全新(green field)项目

### 2. 增量式(混合方式)
- 让 AngularJS 和 Angular 并行运行
- 逐个功能迁移
- 使用 ngUpgrade 实现互操作
- **最适合:** 大型应用、持续交付

### 3. 纵向切片式
- 完整迁移一个功能
- 新功能用 Angular 开发,旧功能保留在 AngularJS 中维护
- 逐步替换
- **最适合:** 中型应用、功能边界清晰的场景

## 混合应用搭建

```typescript
// main.ts - Bootstrap hybrid app
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { UpgradeModule } from '@angular/upgrade/static';
import { AppModule } from './app/app.module';

platformBrowserDynamic()
  .bootstrapModule(AppModule)
  .then(platformRef => {
    const upgrade = platformRef.injector.get(UpgradeModule);
    // Bootstrap AngularJS
    upgrade.bootstrap(document.body, ['myAngularJSApp'], { strictDi: true });
  });
```

```typescript
// app.module.ts
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { UpgradeModule } from '@angular/upgrade/static';

@NgModule({
  imports: [
    BrowserModule,
    UpgradeModule
  ]
})
export class AppModule {
  constructor(private upgrade: UpgradeModule) {}

  ngDoBootstrap() {
    // Bootstrapped manually in main.ts
  }
}
```

## 组件迁移

### AngularJS Controller → Angular Component
```javascript
// Before: AngularJS controller
angular.module('myApp').controller('UserController', function($scope, UserService) {
  $scope.user = {};

  $scope.loadUser = function(id) {
    UserService.getUser(id).then(function(user) {
      $scope.user = user;
    });
  };

  $scope.saveUser = function() {
    UserService.saveUser($scope.user);
  };
});
```

```typescript
// After: Angular component
import { Component, OnInit } from '@angular/core';
import { UserService } from './user.service';

@Component({
  selector: 'app-user',
  template: `
    <div>
      <h2>{{ user.name }}</h2>
      <button (click)="saveUser()">Save</button>
    </div>
  `
})
export class UserComponent implements OnInit {
  user: any = {};

  constructor(private userService: UserService) {}

  ngOnInit() {
    this.loadUser(1);
  }

  loadUser(id: number) {
    this.userService.getUser(id).subscribe(user => {
      this.user = user;
    });
  }

  saveUser() {
    this.userService.saveUser(this.user);
  }
}
```

### AngularJS Directive → Angular Component
```javascript
// Before: AngularJS directive
angular.module('myApp').directive('userCard', function() {
  return {
    restrict: 'E',
    scope: {
      user: '=',
      onDelete: '&'
    },
    template: `
      <div class="card">
        <h3>{{ user.name }}</h3>
        <button ng-click="onDelete()">Delete</button>
      </div>
    `
  };
});
```

```typescript
// After: Angular component
import { Component, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-user-card',
  template: `
    <div class="card">
      <h3>{{ user.name }}</h3>
      <button (click)="delete.emit()">Delete</button>
    </div>
  `
})
export class UserCardComponent {
  @Input() user: any;
  @Output() delete = new EventEmitter<void>();
}

// Usage: <app-user-card [user]="user" (delete)="handleDelete()"></app-user-card>
```

## 服务迁移

```javascript
// Before: AngularJS service
angular.module('myApp').factory('UserService', function($http) {
  return {
    getUser: function(id) {
      return $http.get('/api/users/' + id);
    },
    saveUser: function(user) {
      return $http.post('/api/users', user);
    }
  };
});
```

```typescript
// After: Angular service
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  constructor(private http: HttpClient) {}

  getUser(id: number): Observable<any> {
    return this.http.get(`/api/users/${id}`);
  }

  saveUser(user: any): Observable<any> {
    return this.http.post('/api/users', user);
  }
}
```

## 依赖注入变更

### 降级:Angular → AngularJS
```typescript
// Angular service
import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class NewService {
  getData() {
    return 'data from Angular';
  }
}

// Make available to AngularJS
import { downgradeInjectable } from '@angular/upgrade/static';

angular.module('myApp')
  .factory('newService', downgradeInjectable(NewService));

// Use in AngularJS
angular.module('myApp').controller('OldController', function(newService) {
  console.log(newService.getData());
});
```

### 升级:AngularJS → Angular
```typescript
// AngularJS service
angular.module('myApp').factory('oldService', function() {
  return {
    getData: function() {
      return 'data from AngularJS';
    }
  };
});

// Make available to Angular
import { InjectionToken } from '@angular/core';

export const OLD_SERVICE = new InjectionToken<any>('oldService');

@NgModule({
  providers: [
    {
      provide: OLD_SERVICE,
      useFactory: (i: any) => i.get('oldService'),
      deps: ['$injector']
    }
  ]
})

// Use in Angular
@Component({...})
export class NewComponent {
  constructor(@Inject(OLD_SERVICE) private oldService: any) {
    console.log(this.oldService.getData());
  }
}
```

## 路由迁移

```javascript
// Before: AngularJS routing
angular.module('myApp').config(function($routeProvider) {
  $routeProvider
    .when('/users', {
      template: '<user-list></user-list>'
    })
    .when('/users/:id', {
      template: '<user-detail></user-detail>'
    });
});
```

```typescript
// After: Angular routing
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

const routes: Routes = [
  { path: 'users', component: UserListComponent },
  { path: 'users/:id', component: UserDetailComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}
```

## 表单迁移

```html
<!-- Before: AngularJS -->
<form name="userForm" ng-submit="saveUser()">
  <input type="text" ng-model="user.name" required>
  <input type="email" ng-model="user.email" required>
  <button ng-disabled="userForm.$invalid">Save</button>
</form>
```

```typescript
// After: Angular (Template-driven)
@Component({
  template: `
    <form #userForm="ngForm" (ngSubmit)="saveUser()">
      <input type="text" [(ngModel)]="user.name" name="name" required>
      <input type="email" [(ngModel)]="user.email" name="email" required>
      <button [disabled]="userForm.invalid">Save</button>
    </form>
  `
})

// Or Reactive Forms (preferred)
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  template: `
    <form [formGroup]="userForm" (ngSubmit)="saveUser()">
      <input formControlName="name">
      <input formControlName="email">
      <button [disabled]="userForm.invalid">Save</button>
    </form>
  `
})
export class UserFormComponent {
  userForm: FormGroup;

  constructor(private fb: FormBuilder) {
    this.userForm = this.fb.group({
      name: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]]
    });
  }

  saveUser() {
    console.log(this.userForm.value);
  }
}
```

## 迁移时间线

```
Phase 1: Setup (1-2 weeks)
- Install Angular CLI
- Set up hybrid app
- Configure build tools
- Set up testing

Phase 2: Infrastructure (2-4 weeks)
- Migrate services
- Migrate utilities
- Set up routing
- Migrate shared components

Phase 3: Feature Migration (varies)
- Migrate feature by feature
- Test thoroughly
- Deploy incrementally

Phase 4: Cleanup (1-2 weeks)
- Remove AngularJS code
- Remove ngUpgrade
- Optimize bundle
- Final testing
```

## 资源

- **references/hybrid-mode.md**: 混合应用模式
- **references/component-migration.md**: 组件转换指南
- **references/dependency-injection.md**: 依赖注入迁移策略
- **references/routing.md**: 路由迁移
- **assets/hybrid-bootstrap.ts**: 混合应用模板
- **assets/migration-timeline.md**: 项目规划
- **scripts/analyze-angular-app.sh**: 应用分析脚本

## 最佳实践

1. **从服务开始**: 先迁移服务(更简单)
2. **增量方式**: 逐个功能迁移
3. **持续测试**: 每一步都要测试
4. **使用 TypeScript**: 尽早迁移到 TypeScript
5. **遵循风格指南**: 从第一天起就遵循 Angular 风格指南
6. **稍后优化**: 先让它跑起来,然后再优化
7. **记录文档**: 保留迁移笔记

## 常见陷阱

- 混合应用没有正确搭建
- 在迁移逻辑之前就迁移了 UI
- 忽视了变更检测机制的差异
- 没有正确处理 scope
- 混用两种模式(AngularJS + Angular)
- 测试不充分

## 局限性
- 仅在任务明显符合上述描述的范围时使用本技能。
- 不要将输出当作替代环境特定验证、测试或专家评审的手段。
- 如果所需的输入、权限、安全边界或成功标准缺失,应停下并要求澄清。
