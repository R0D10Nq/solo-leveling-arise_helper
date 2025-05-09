def generate_analytics(profile, characters, artifacts):
    report = []
    if not characters:
        return 'Нет данных о персонажах.'
    report.append('Аналитика по команде\n')
    tank_count = 0
    dps_count = 0
    support_count = 0
    used_arts = set()
    class_roles = []
    art_names = set(a['name'] for a in artifacts)
    # Индивидуальные советы по каждому персонажу
    for idx, c in enumerate(characters):
        stats = {k: c.get(k, 0) for k in ['hp','atk','def','crit']}
        # Артефакт для персонажа (если назначение будет реализовано)
        art = artifacts[idx] if idx < len(artifacts) else None
        if art:
            for k, v in art['bonus'].items():
                stats[k] = stats.get(k, 0) + v
            used_arts.add(art['name'])
        report.append(f"{c['name']} ({c['class']}, {c['rank']}): ")
        report.append(f"  HP: {stats.get('hp',0)} | ATK: {stats.get('atk',0)} | DEF: {stats.get('def',0)} | CRIT: {stats.get('crit',0)}")
        role = c.get('class','').lower()
        class_roles.append(role)
        if 'танк' in role or 'tank' in role:
            tank_count += 1
        elif 'dps' in role or 'damage' in role or 'монарх' in role:
            dps_count += 1
        elif 'support' in role or 'саппорт' in role or 'heal' in role:
            support_count += 1
        # Индивидуальные советы
        if not art:
            report.append('  ⚠ Нет назначенного артефакта!')
        elif 'atk' in art['bonus'] and stats['atk'] < 1000:
            report.append('  ⓘ Можно усилить атаку этим артефактом.')
        elif 'def' in art['bonus'] and stats['def'] < 500:
            report.append('  ⓘ Рекомендуется повысить защиту.')
    report.append('\nРекомендации:')
    if tank_count == 0:
        report.append('- Добавьте персонажа с ролью танк для выживаемости.')
    if dps_count == 0:
        report.append('- Добавьте дамагера для повышения урона.')
    if support_count == 0:
        report.append('- Добавьте саппорта для усиления команды.')
    if len(artifacts) < len(characters):
        report.append('- Не всем персонажам назначены артефакты.')
    if len(artifacts) > 0:
        report.append(f'- Используются артефакты: {", ".join(art_names)}')
    if len(art_names) != len(artifacts):
        report.append('- Есть повторяющиеся артефакты — лучше разнообразить экипировку.')
    if len(set(class_roles)) == 1:
        report.append('- Все персонажи одной роли — попробуйте добавить разные классы для баланса.')
    return "\n".join(report)
