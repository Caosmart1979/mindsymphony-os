---
name: linear-task-manager
description: Linear issue and project management integration. Connects Linear tasks with MindSymphony Boulder State tracking for seamless task synchronization and workflow management.
---

# Linear Task Manager

Linear integration for MindSymphony, enabling seamless connection between Linear issues and Boulder State task tracking.

## When to Use

- Syncing Linear issues with local Boulder State tasks
- Managing project milestones across Linear and MindSymphony
- Tracking issue status changes
- Automating task workflows between Linear and local development

## Core Capabilities

### 1. Task Synchronization

**Sync Linear Issue to Boulder State:**
```yaml
linear_issue:
  id: TEAM-123
  title: "Implement user authentication"
  state: "In Progress"
  assignee: "developer"
  priority: "High"

boulder_state_mapping:
  task_id: "linear-TEAM-123"
  status: "in_progress"
  blocks: []
  created: "2024-01-15T10:00:00Z"
```

### 2. Status Mapping

| Linear State | Boulder State |
|-------------|---------------|
| Backlog | pending |
| Todo | pending |
| In Progress | in_progress |
| In Review | in_progress |
| Done | completed |
| Canceled | deleted |

### 3. Workflow Integration

**Create Boulder State Task from Linear:**
```bash
# When Linear webhook received
1. Extract issue details
2. Create Boulder State task
3. Map Linear ID to local task ID
4. Track cross-system references
```

**Update Linear from Boulder State:**
```bash
# When local task completed
1. Find associated Linear issue
2. Update Linear state to "Done"
3. Add comment with completion notes
```

## Integration Patterns

### Pattern 1: Bidirectional Sync
```
Linear ←──→ MindSymphony
   │           │
   │ Webhook   │ Boulder State
   │           │
   └── Issue ──┘ Task
```

### Pattern 2: Linear as Source of Truth
```
Linear (Plan) → MindSymphony (Execute) → Linear (Report)
     ↑                                        ↓
   Issues                                Updates
```

### Pattern 3: Local-First with Linear Backup
```
MindSymphony Boulder State (Primary)
              ↓
         Periodic Sync
              ↓
      Linear (Backup/Visibility)
```

## Configuration

### Environment Variables
```bash
LINEAR_API_KEY=lin_api_xxxxxxxxxxxx
LINEAR_TEAM_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
LINEAR_WEBHOOK_SECRET=whsec_xxxxxxxxxxxx
```

### Boulder State Integration
```yaml
# In task metadata
task:
  id: "task-001"
  subject: "Implement auth flow"
  linear:
    issue_id: "TEAM-123"
    url: "https://linear.app/team/issue/TEAM-123"
    last_sync: "2024-01-15T10:00:00Z"
```

## Commands

### Sync Commands
```bash
# Sync specific issue
linear-sync TEAM-123

# Sync all assigned issues
linear-sync --assigned

# Sync by state
linear-sync --state "In Progress"

# Full sync
linear-sync --all
```

### Task Management
```bash
# Create Linear issue from Boulder State
linear-create "Bug: Login fails" --priority high

# Update Linear status
linear-update TEAM-123 --state "In Review"

# Add comment
linear-comment TEAM-123 "Fix implemented, testing now"
```

## Integration with Other Skills

### With cognitive-architect
- Pull Linear epics as project boundaries
- Create Boulder State tasks for each Linear issue
- Track cross-task dependencies

### With task-enforcer
- Boulder State tasks automatically sync to Linear
- Linear updates reflected in Boulder State
- Unified task tracking across systems

### With git-workflow
- Linear issue ID in commit messages
- Automatic PR linking to Linear issues
- Branch naming: `feature/TEAM-123-description`

## Best Practices

1. **Always use Linear ID in Boulder State metadata** for traceability
2. **Keep statuses in sync** to avoid confusion
3. **Use Linear for planning**, MindSymphony for execution
4. **Comment on Linear** when significant progress made
5. **Close Linear issues** only after Boulder State task completed

## Troubleshooting

**Issue: Sync fails**
- Check LINEAR_API_KEY is valid
- Verify network connectivity
- Check Linear API rate limits

**Issue: Status mismatch**
- Run `linear-sync --force` to re-sync
- Check status mapping configuration
- Verify webhook delivery

**Issue: Duplicate tasks**
- Use consistent ID mapping
- Check for case sensitivity in issue IDs
- Verify webhook deduplication

## Security Notes

- Store LINEAR_API_KEY in environment variables only
- Never commit API keys to git
- Use webhook secrets to verify Linear payloads
- Rotate API keys regularly

## Resources

- [Linear API Documentation](https://developers.linear.app/)
- [Linear Webhooks](https://developers.linear.app/docs/graphql/webhooks)
- [MindSymphony Boulder State](docs/boulder-state.md)
